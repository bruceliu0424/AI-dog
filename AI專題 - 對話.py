# -*- coding: utf-8 -*-
import requests

# 請將這裡的 YOUR_API_KEY 替換為你的 OpenAI API 金鑰
api_key = "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"
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 初始化對話歷史
messages = []

def chat_with_model(user_input):
    # 將用戶輸入添加到對話歷史中
    messages.append({"role": "user", "content": user_input})

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']['content']
        # 將機器人的回應添加到對話歷史中
        messages.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    else:
        return f"錯誤: {response.status_code}, {response.text}"

# 主對話循環
if __name__ == "__main__":
    print("與機器人聊天，輸入 'exit' 以結束對話。")
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'exit':
            print("結束對話。")
            break
        response = chat_with_model(user_input)
        print("機器人:", response)