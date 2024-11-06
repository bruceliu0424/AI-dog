import requests
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageDraw

# 請替換成你的 OpenAI API 金鑰
api_key = ""
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 初始化對話歷史
messages = []

def chat_with_model(user_input):
    messages.append({"role": "user", "content": user_input})

    data = {
        "model": "gpt-4o-mini",  # 確保使用正確的模型名稱
        "messages": messages,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    else:
        return f"錯誤: {response.status_code}, {response.text}"

def send_message():
    user_input = entry.get()
    if user_input.lower() == 'exit':
        root.quit()
    else:
        display_message(user_input, user_avatar, "你")
        entry.delete(0, tk.END)

        response = chat_with_model(user_input)
        display_message(response, bot_avatar, "機器人")

def display_message(message, avatar, sender):
    chat_area.config(state=tk.NORMAL)
    chat_area.image_create(tk.END, image=avatar)  # 添加頭像
    chat_area.insert(tk.END, f" {sender}: {message}\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)  # 滾動到最後一行

def create_circle_avatar(image_path, size=(30, 30)):
    img = Image.open(image_path).resize(size, Image.LANCZOS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)

# 建立主窗口
root = tk.Tk()
root.title("聊天機器人")
root.geometry("400x500")

# 聊天區域
chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# 輸入框
entry = tk.Entry(root, width=50)
entry.pack(pady=10, padx=10)

# 發送按鈕
send_button = tk.Button(root, text="發送", command=send_message)
send_button.pack(pady=5)

# 加載並生成圓形頭像
user_avatar = create_circle_avatar("user_avatar.jpg")
bot_avatar = create_circle_avatar("bot_avatar.jpg")

# 開始主循環
root.mainloop()
