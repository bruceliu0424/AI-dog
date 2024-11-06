# -*- coding: utf-8 -*-
import requests

# 你的 40 Mini API 金鑰
api_key = ""
api_url = "https://ncuedu.tw/mygpts/2200/4408"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
def test_api_key():
    test_message = "測試金鑰的有效性。"
    data = {
        "messages": [{"role": "user", "content": test_message}]
    }
    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        print("金鑰有效，API 響應：", response.json())
    else:
        print("金鑰無效或有其他錯誤，狀態碼：", response.status_code)
        print("返回內容：", response.text)

test_api_key()
conversation_history = []

def send_message(message):
    # 更新對話歷史
    conversation_history.append({"role": "user", "content": message})

    # 準備發送的數據
    data = {
        "messages": conversation_history
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        bot_reply = response.json().get("message")
        # 更新對話歷史，添加機器人的回應
        conversation_history.append({"role": "assistant", "content": bot_reply})
        return bot_reply
    else:
        return f"Error: {response.status_code}"

# 測試對話
while True:
    user_input = input("輸入你想說的話 (輸入 'exit' 以結束)：")
    if user_input.lower() == 'exit':
        break
    result = send_message(user_input)
    print("機器人的回應：", result)
