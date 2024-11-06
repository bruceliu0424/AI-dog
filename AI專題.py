# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def fetch_restaurants():
    url = "https://www.taiwan.net.tw/m1.aspx?sNo=0020118"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        restaurant_data = []

        # 根據實際的 HTML 結構抓取餐廳信息
        rows = soup.find_all('tr', attrs={"data-open": True})  # 只抓取帶有 data-open 屬性的行
        for row in rows:
            name = row.find('td', class_='name').text.strip()  # 餐廳名稱
            
            # 找到下一个 tr 元素中的更多信息
            more_info_row = row.find_next_sibling('tr')
            if more_info_row:
                # 先找電話
                phone_div = more_info_row.find(text=lambda x: x and '電話：' in x)
                phone = phone_div.find_next().text.strip() if phone_div else '未提供'
                
                # 再找地址
                address_div = more_info_row.find(text=lambda x: x and '地址：' in x)
                address = address_div.find_next().text.strip() if address_div else '未提供'
                
                restaurant_data.append({
                    "名稱": name,
                    "地址": address,
                    "電話": phone
                })
        return restaurant_data
    else:
        messagebox.showerror("錯誤", "無法從網站獲取數據。")
        return []

# 查询餐厅函数
def find_restaurant():
    restaurant_name = entry.get().strip()  # 获取并去除空白
    for restaurant in restaurants:
        if restaurant["名稱"] == restaurant_name:
            address = restaurant["地址"]
            phone = restaurant["電話"]
            result = f"地址: {address}\n電話: {phone}"
            messagebox.showinfo("餐廳信息", result)
            return
    messagebox.showwarning("警告", "未找到該餐廳的信息。")

# 抓取餐厅数据
restaurants = fetch_restaurants()

# 创建主窗口
root = tk.Tk()
root.title("穆斯林餐廳查詢機器人")

# 创建输入框
entry_label = tk.Label(root, text="輸入餐廳名稱:")
entry_label.pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# 创建查询按钮
query_button = tk.Button(root, text="查詢餐廳", command=find_restaurant)
query_button.pack(pady=10)

# 启动主事件循环
root.mainloop()
