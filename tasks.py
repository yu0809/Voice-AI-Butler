# -*- coding: utf-8 -*-
# tasks.py
from datetime import datetime

def get_current_task(beijing_time):
    schedule = [
        (8, "做数学作业。记得在9:00开始做英语作业哦！", "images/gif1.gif"),
        (9, "做英语作业。记得在10:00开始做科学作业哦！", "images/gif2.gif"),
        (10, "做科学作业。记得在11:00开始做历史作业哦！", "images/gif3.gif"),
        (11, "做历史作业。记得在12:00开始吃午饭哦！", "images/gif4.gif"),
        (12, "吃午饭和休息。记得在13:00开始做地理作业哦！", "images/gif5.gif"),
        (13, "做地理作业。记得在14:00开始做美术作业哦！", "images/gif6.gif"),
        (14, "做美术作业。记得在15:00开始做音乐练习哦！", "images/gif7.gif"),
        (15, "做音乐练习。记得在16:00开始做物理作业哦！", "images/gif8.gif"),
        (16, "做物理作业。记得在17:00开始做生物作业哦！", "images/gif9.gif"),
        (17, "做生物作业。记得在18:00开始吃晚饭哦！", "images/gif10.gif"),
        (18, "吃晚饭和休息。记得在19:00开始做社会学作业哦！", "images/gif11.gif"),
        (19, "做社会学作业。记得在20:00开始做体育练习哦！", "images/gif12.gif"),
        (20, "做体育练习。记得在21:00开始准备睡觉哦！", "images/gif13.gif"),
        (21, "准备睡觉。记得明天8:00开始新一天的学习计划哦！", "images/gif14.gif"),
    ]

    current_hour = beijing_time.hour
    current_minute = beijing_time.minute

    for hour, task, image in schedule:
        if current_hour == hour:
            if current_minute == 0:
                return f"现在是{beijing_time.strftime('%H:%M')}，{task}", image
            else:
                next_hour = hour + 1
                next_task = next(
                    (t.split('。记得在')[0] for h, t, img in schedule if h == next_hour), "完成所有任务"
                )
                current_task = task.split('。记得在')[0]
                return f"现在是{beijing_time.strftime('%H:%M')}，继续{current_task}。记得在{next_hour}:00开始{next_task}哦！^_^", image
        elif current_hour < hour:
            next_task = task.split('。记得在')[0]
            return f"现在是{beijing_time.strftime('%H:%M')}，继续当前的任务。记得在{hour}:00开始{next_task}哦！^_^", image
    return "现在是休息时间，没有安排任务哦！^_^", None

def get_robot_daily_schedule():
    # 定义固定的机器人日常任务安排
    schedule = [
        {"hour": 8, "task": "检查系统状态"},
        {"hour": 9, "task": "进行数据备份"},
        {"hour": 10, "task": "自我诊断"},
        {"hour": 11, "task": "维护硬件"},
        {"hour": 12, "task": "休息时间"},
        {"hour": 13, "task": "与其他机器人同步"},
        {"hour": 14, "task": "执行例行任务"},
        {"hour": 15, "task": "学习新技能"},
        {"hour": 16, "task": "用户交互准备"},
        {"hour": 17, "task": "记录交互日志"},
        {"hour": 18, "task": "数据分析"},
        {"hour": 19, "task": "充电"},
        {"hour": 20, "task": "检查安全系统"},
        {"hour": 21, "task": "待机模式"}
    ]
    return schedule

def get_robot_current_task(beijing_time, schedule):
    current_hour = beijing_time.hour
    current_minute = beijing_time.minute

    for i, entry in enumerate(schedule):
        hour = entry["hour"]
        task = entry["task"]
        if current_hour == hour:
            if current_minute == 0:
                if i + 1 < len(schedule):
                    next_hour = schedule[i + 1]["hour"]
                    next_task = schedule[i + 1]["task"]
                else:
                    next_hour = "无任务安排"
                    next_task = "无任务安排"
                return f"现在是{beijing_time.strftime('%H:%M')}，我在{task}哦。我会在{next_hour}:00开始{next_task}哦！(●′ω●)"
            else:
                if i + 1 < len(schedule):
                    next_hour = schedule[i + 1]["hour"]
                    next_task = schedule[i + 1]["task"]
                else:
                    next_hour = "无任务安排"
                    next_task = "无任务安排"
                return f"现在是{beijing_time.strftime('%H:%M')}，我在{task}哦。我会在{next_hour}:00开始{next_task}哦！(●′ω●)"
        elif current_hour < hour:
            next_task = task
            return f"现在是{beijing_time.strftime('%H:%M')}，我在{next_task}哦。我会在{hour}:00开始{next_task}哦！(●′ω●)"
    return "现在是休息时间，没有安排任务哦！^_^"