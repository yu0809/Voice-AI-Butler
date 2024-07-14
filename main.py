# -*- coding: utf-8 -*-
# main.py
import threading
import time
import queue
from api import chat_completion, summarize_conversation
from utils import get_beijing_time
from tasks import get_current_task, get_robot_current_task, get_robot_daily_schedule
from gui import display_image_with_time
from speech_recognition import recognize_speech_from_mic
from emotion_detection import start_emotion_detection
import json

def emotion_detection_thread(stop_event, message_queue):
    start_emotion_detection(5, stop_event)
    while not stop_event.is_set():
        time.sleep(1)
        message_queue.put("Emotion detected")

def log_conversation(input_text, output_text):
    # 追加新对话到日志文件中，而不是覆盖
    with open("conversation_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"User: {input_text}\n")
        log_file.write(f"Assistant: {output_text}\n")
        log_file.write("\n")

def load_conversation_log():
    try:
        with open("conversation_log.txt", "r", encoding="utf-8") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return ""

def save_conversation_log(summary):
    with open("conversation_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(summary)

def daily_schedule_thread(stop_event, pause_event, schedule):
    while not stop_event.is_set():
        if not pause_event.is_set():
            show_robot_schedule(schedule)
            time.sleep(60)  # 每分钟检查一次任务
        else:
            pause_event.wait()  # 等待暂停结束

def show_robot_schedule(schedule):
    current_time = get_beijing_time()
    current_task = get_robot_current_task(current_time, schedule)
    print(f"当前北京时间是：{current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(current_task)

def main():
    messages = []
    max_context_length = 2048
    message_queue = queue.Queue()

    # 获取机器人的日常任务安排
    try:
        robot_schedule = get_robot_daily_schedule()
    except Exception as e:
        print(f"获取机器人任务安排失败: {e}")
        return

    stop_event = threading.Event()
    pause_event = threading.Event()

    # 启动机器人日常任务线程
    threading.Thread(target=daily_schedule_thread, args=(stop_event, pause_event, robot_schedule)).start()

    while True:
        show_robot_schedule(robot_schedule)  # 显示机器人的日常任务
        enter_interaction = input("你想进入交互模式吗？（是/否）：")
        if enter_interaction.lower() in ['是', 'y', 'yes']:
            pause_event.set()  # 暂停日常任务显示
            system_message = input("你希望我成为什么类型的聊天机器人？")
            system_message = {"role": "system", "content": system_message}

            # 获取用户当天的任务安排
            current_time = get_beijing_time()
            current_task, image_path = get_current_task(current_time)
            print(f"当前北京时间是：{current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(current_task)

            if image_path:
                display_image_with_time(image_path)

            print(f"好的！我已经准备好成为你的{system_message['content']}。在完成任务的过程中有遇到什么困难吗？请告诉我。")

            first_question = True

            while True:
                start_question = input("你想开始问问题吗？（是/否）：")
                if start_question.lower() in ['是', 'y', 'yes']:
                    print("请开始说话...")
                    user_message = recognize_speech_from_mic()

                    if user_message:
                        print(f"识别到的语音: {user_message}")
                        if user_message.lower() in ['退出', '结束', 'quit', 'exit']:
                            print("对话已结束。")
                            break

                        if first_question:
                            # 启动情绪检测线程，仅在第一轮对话时运行
                            emotion_detection_stop_event = threading.Event()
                            threading.Thread(target=emotion_detection_thread, args=(emotion_detection_stop_event, message_queue)).start()
                            first_question = False

                        # 读取并精简记忆库
                        conversation_log = load_conversation_log()
                        prompt_file = "prompt.txt"  # 预先定义好的侧重需求文件
                        try:
                            summary = summarize_conversation(conversation_log, user_message, prompt_file)
                            save_conversation_log(summary)  # 更新记忆库内容
                        except Exception as e:
                            print(f"Error summarizing conversation: {e}")
                            continue

                        # 使用精简后的记忆库和当前用户输入
                        messages = [{"role": "user", "content": summary}, {"role": "user", "content": user_message}]

                        # 确保消息总数为奇数，且交替角色
                        if len(messages) % 2 == 0:
                            messages.insert(1, {"role": "assistant", "content": "这是一个占位系统消息，用于确保消息总数为奇数。"})

                        try:
                            response = chat_completion(messages)
                            print(f"API响应: {response}")
                            assistant_reply = response.get('result')
                            if assistant_reply:
                                print("文心一言: " + assistant_reply)
                                log_conversation(user_message, assistant_reply)  # 记录对话
                            else:
                                print("API响应中未找到'result'字段。")
                        except Exception as e:
                            print(f"请求失败: {e}")

                    while not message_queue.empty():
                        message_queue.get()

                    continue_question = input("你想继续问问题吗？（是/否）：")
                    if continue_question.lower() not in ['是', 'y', 'yes']:
                        break

            pause_event.clear()  # 恢复日常任务显示
            show_robot_schedule(robot_schedule)  # 显示机器人的日常任务

    stop_event.set()

if __name__ == "__main__":
    main()