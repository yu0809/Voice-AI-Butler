# -*- coding: utf-8 -*-
# gui.py
import os
import tkinter as tk
from PIL import Image, ImageTk
from utils import get_beijing_time

def display_image_with_time(image_path):
    if os.path.exists(image_path):
        root = tk.Tk()
        root.title("图片展示和实时时间")

        def update_time():
            current_time = get_beijing_time().strftime('%Y-%m-%d %H:%M:%S')
            time_label.config(text=f"当前北京时间是：{current_time}")
            root.after(1000, update_time)

        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(root, image=img)
        img_label.pack()

        time_label = tk.Label(root, text="", font=("Helvetica", 16))
        time_label.pack()

        update_time()
        root.mainloop()
        input("按Enter键关闭图片后继续...")
    else:
        print(f"图片 {image_path} 不存在。")