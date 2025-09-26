#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox

def simple_email_input():
    print("🚀 启动邮箱输入窗口...")
    
    root = tk.Tk()
    root.title("邮箱输入 - 简单版")
    
    # 设置窗口大小和位置 - 固定在屏幕左上角
    root.geometry("500x300+50+50")
    root.configure(bg="white")
    
    # 强制窗口显示在最前面 - 修复macOS显示问题
    root.lift()
    root.attributes('-topmost', True)
    root.focus_force()
    
    # 确保窗口可见 - 修复透明/不可见问题
    root.update()
    root.deiconify()  # 确保窗口不是最小化状态
    root.state('normal')  # 确保窗口是正常状态
    
    # 大标题 - 使用更明显的颜色
    title = tk.Label(root, text="📧 邮箱输入", 
                    font=("Arial", 20, "bold"), 
                    bg="yellow", fg="red",  # 黄色背景，红色文字
                    relief="raised", bd=3)  # 3D边框效果
    title.pack(pady=30)
    
    # 说明文字
    info = tk.Label(root, text="请输入您的邮箱地址：", 
                   font=("Arial", 12), 
                   bg="white", fg="black")
    info.pack(pady=10)
    
    # 输入框 - 更明显的样式
    email_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=email_var, 
                    font=("Arial", 16), width=40,
                    bg="lightblue", fg="darkblue",  # 浅蓝背景，深蓝文字
                    relief="raised", bd=4)  # 4像素边框
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
    
    # 按钮
    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(pady=20)
    
    submit_btn = tk.Button(button_frame, text="确认", command=submit,
                          font=("Arial", 12), bg="green", fg="white",
                          padx=30, pady=10)
    submit_btn.pack(side=tk.LEFT, padx=10)
    
    cancel_btn = tk.Button(button_frame, text="取消", command=cancel,
                          font=("Arial", 12), bg="red", fg="white",
                          padx=30, pady=10)
    cancel_btn.pack(side=tk.LEFT, padx=10)
    
    # 绑定回车键
    entry.bind('<Return>', lambda e: submit())
    
    print("📱 窗口应该已经显示，请查看屏幕左上角...")
    
    root.mainloop()
    return result["email"]

if __name__ == "__main__":
    print("=" * 50)
    print("开始运行邮箱输入程序")
    print("=" * 50)
    
    email = simple_email_input()
    
    print("=" * 50)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 50)
