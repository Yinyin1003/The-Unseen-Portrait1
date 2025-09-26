#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import sys

def fixed_email_input():
    print("🚀 启动邮箱输入窗口...")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("邮箱输入")
    
    # 设置窗口大小和位置
    root.geometry("600x400+100+100")
    
    # 设置背景色为明显的颜色
    root.configure(bg="lightgray")
    
    # 强制窗口显示
    root.lift()
    root.attributes('-topmost', True)
    root.focus_force()
    
    # 等待窗口完全初始化
    root.update_idletasks()
    
    # 创建主框架
    main_frame = tk.Frame(root, bg="white", relief="raised", bd=5)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # 大标题 - 使用非常明显的颜色
    title = tk.Label(main_frame, text="📧 邮箱输入", 
                    font=("Arial", 24, "bold"), 
                    bg="red", fg="white",  # 红色背景，白色文字
                    relief="raised", bd=3)
    title.pack(pady=20)
    
    # 说明文字
    info = tk.Label(main_frame, text="请输入您的邮箱地址：", 
                   font=("Arial", 14), 
                   bg="white", fg="black")
    info.pack(pady=10)
    
    # 输入框
    email_var = tk.StringVar()
    entry = tk.Entry(main_frame, textvariable=email_var, 
                    font=("Arial", 16), width=50,
                    bg="lightblue", fg="darkblue",
                    relief="raised", bd=3)
    entry.pack(pady=20)
    entry.focus()
    
    result = {"email": None}
    
    def submit():
        email = email_var.get().strip()
        if email:
            result["email"] = email
            print(f"✅ 用户输入邮箱: {email}")
            root.destroy()
        else:
            messagebox.showwarning("提示", "请输入邮箱地址")
    
    def cancel():
        print("❌ 用户取消输入")
        root.destroy()
    
    # 按钮框架
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(pady=20)
    
    # 确认按钮
    submit_btn = tk.Button(button_frame, text="确认", command=submit,
                          font=("Arial", 14, "bold"), bg="green", fg="white",
                          padx=30, pady=10, relief="raised", bd=3)
    submit_btn.pack(side=tk.LEFT, padx=10)
    
    # 取消按钮
    cancel_btn = tk.Button(button_frame, text="取消", command=cancel,
                          font=("Arial", 14, "bold"), bg="red", fg="white",
                          padx=30, pady=10, relief="raised", bd=3)
    cancel_btn.pack(side=tk.LEFT, padx=10)
    
    # 绑定回车键
    entry.bind('<Return>', lambda e: submit())
    
    # 强制更新显示
    root.update()
    
    print("📱 窗口应该已经显示，请查看屏幕...")
    
    # 运行主循环
    root.mainloop()
    return result["email"]

if __name__ == "__main__":
    print("=" * 50)
    print("开始运行邮箱输入程序")
    print("=" * 50)
    
    email = fixed_email_input()
    
    print("=" * 50)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 50)
