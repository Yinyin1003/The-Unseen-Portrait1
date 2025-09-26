#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import re

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_email_input():
    root = tk.Tk()
    root.title("邮箱输入")
    
    # 确保窗口在最前面
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))

    # 固定窗口大小并居中
    width, height = 400, 300   # 高度更大，保证能看到
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)
    
    # 设置窗口背景色
    root.configure(bg="#f8f9fa")

    result = {"email": None}

    # 标题
    title = tk.Label(root, text="请输入邮箱地址", font=("Arial", 14, "bold"), bg="#f8f9fa")
    title.pack(pady=20)

    # 输入框
    email_var = tk.StringVar()
    entry = tk.Entry(
        root,
        textvariable=email_var,
        font=("Arial", 12),
        width=30,
        bg="#ffffff",         # 白色背景
        fg="#000000",         # 黑色文字
        highlightthickness=1, # 边框厚度
        highlightbackground="#999999", # 未聚焦时边框颜色
        highlightcolor="#007bff"       # 聚焦时边框颜色
    )
    entry.pack(pady=20)   # 加大 padding
    entry.focus()

    # 按钮事件
    def submit():
        email = email_var.get().strip()
        if not email:
            messagebox.showerror("错误", "请输入邮箱地址")
            return
        if not validate_email(email):
            messagebox.showerror("错误", "请输入有效的邮箱地址 (例如 user@example.com)")
            return
        result["email"] = email
        root.destroy()

    def cancel():
        result["email"] = None
        root.destroy()

    # 按钮框架
    button_frame = tk.Frame(root, bg="#f8f9fa")
    button_frame.pack(pady=20)

    submit_btn = tk.Button(button_frame, text="确认", command=submit,
                          font=("Arial", 12), bg="#007bff", fg="white",
                          padx=20, pady=5)
    submit_btn.pack(side=tk.LEFT, padx=10)

    cancel_btn = tk.Button(button_frame, text="取消", command=cancel,
                          font=("Arial", 12), bg="#6c757d", fg="white",
                          padx=20, pady=5)
    cancel_btn.pack(side=tk.LEFT, padx=10)

    # 绑定回车键
    entry.bind('<Return>', lambda e: submit())

    root.mainloop()
    return result["email"]

if __name__ == "__main__":
    email = get_email_input()
    if email:
        print(f"✅ 输入的邮箱: {email}")
    else:
        print("❌ 未输入邮箱或用户取消")
