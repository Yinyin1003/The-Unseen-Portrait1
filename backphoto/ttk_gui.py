#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import re

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def ttk_email_input():
    """使用ttk创建现代化邮箱输入界面"""
    print("🚀 启动TTK邮箱输入窗口...")
    
    root = tk.Tk()
    root.title("邮箱输入 - TTK版本")
    root.geometry("500x400+200+200")
    
    # 创建样式
    style = ttk.Style()
    
    # 设置主题
    style.theme_use('clam')  # 使用clam主题，更现代
    
    # 自定义样式
    style.configure('Title.TLabel', 
                   font=('Arial', 16, 'bold'),
                   foreground='#2c3e50',
                   background='white')
    
    style.configure('Info.TLabel',
                   font=('Arial', 12),
                   foreground='#34495e',
                   background='white')
    
    style.configure('Custom.TEntry',
                   font=('Arial', 12),
                   fieldbackground='#ecf0f1',
                   borderwidth=2,
                   relief='solid')
    
    style.configure('Submit.TButton',
                   font=('Arial', 12, 'bold'),
                   foreground='white',
                   background='#27ae60',
                   padding=(20, 10))
    
    style.configure('Cancel.TButton',
                   font=('Arial', 12, 'bold'),
                   foreground='white',
                   background='#e74c3c',
                   padding=(20, 10))
    
    # 主框架
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 配置网格权重
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    
    result = {"email": None}
    
    # 标题
    title = ttk.Label(main_frame, text="📧 邮箱输入", style='Title.TLabel')
    title.grid(row=0, column=0, pady=(0, 20))
    
    # 说明
    info = ttk.Label(main_frame, text="请输入您的邮箱地址：", style='Info.TLabel')
    info.grid(row=1, column=0, pady=(0, 10))
    
    # 输入框
    email_var = tk.StringVar()
    entry = ttk.Entry(main_frame, textvariable=email_var, style='Custom.TEntry', width=40)
    entry.grid(row=2, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
    entry.focus()
    
    # 按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, pady=(0, 20))
    
    def submit():
        email = email_var.get().strip()
        if not email:
            messagebox.showerror("错误", "请输入邮箱地址")
            return
        if not validate_email(email):
            messagebox.showerror("错误", "请输入有效的邮箱地址")
            return
        result["email"] = email
        print(f"✅ 用户输入邮箱: {email}")
        root.destroy()
    
    def cancel():
        print("❌ 用户取消输入")
        root.destroy()
    
    # 按钮
    submit_btn = ttk.Button(button_frame, text="确认", command=submit, style='Submit.TButton')
    submit_btn.grid(row=0, column=0, padx=(0, 10))
    
    cancel_btn = ttk.Button(button_frame, text="取消", command=cancel, style='Cancel.TButton')
    cancel_btn.grid(row=0, column=1)
    
    # 绑定回车键
    entry.bind('<Return>', lambda e: submit())
    
    # 强制显示
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    
    print("📱 TTK窗口应该已经显示...")
    
    root.mainloop()
    return result["email"]

if __name__ == "__main__":
    print("=" * 50)
    print("开始运行TTK邮箱输入程序")
    print("=" * 50)
    
    email = ttk_email_input()
    
    print("=" * 50)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 50)
