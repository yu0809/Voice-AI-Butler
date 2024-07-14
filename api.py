# -*- coding: utf-8 -*-
# api.py
import requests
import json
from config import api_endpoint, api_key, secret_key
from utils import get_access_token

access_token = get_access_token(api_key, secret_key)

def chat_completion(messages):
    url = f"{api_endpoint}?access_token={access_token}"
    payload = {
        "messages": messages
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            raise Exception(f"JSON解析错误: {response.text}")
    else:
        raise Exception(f"请求失败: {response.status_code}, {response.text}")

def summarize_conversation(conversation_log, current_input, prompt_file):
    with open(prompt_file, "r", encoding="utf-8") as file:
        prompt_template = file.read()

    # 插入记忆库内容和当前输入
    prompt = prompt_template.replace("<<这里将插入记忆库中的对话内容>>", conversation_log)
    prompt = prompt.replace("<<这里将插入当前的用户输入>>", current_input)

    messages = [{"role": "user", "content": prompt}]
    summary_response = chat_completion(messages)
    summary_result = summary_response.get('result')

    if summary_result is None:
        raise Exception(f"Summary response did not contain 'result' field: {summary_response}")

    # 如果原始对话内容少于2000字，则保留所有内容
    if len(conversation_log) < 2000:
        return conversation_log
    # 如果原始对话内容超过2000字，则使用摘要，并且摘要尽量接近2000字
    elif len(summary_result) > 2000:
        return summary_result[:2000]
    else:
        return summary_result
