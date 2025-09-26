#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Input GUI
Graphical interface for email input
"""

import tkinter as tk
from tkinter import messagebox
import re

class EmailInputGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The Unseen Portrait - Email Input")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 设置窗口居中
        self.center_window()
        
        self.email = None
        self.setup_ui()
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = tk.Frame(self.root, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="🎭 The Unseen Portrait", 
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 15))
        
        # 说明文字
        desc_label = tk.Label(
            main_frame,
            text="Please enter the recipient's email address:",
            font=("Arial", 13),
            fg="#34495e"
        )
        desc_label.pack(pady=(0, 25))
        
        # 邮箱输入框架
        email_frame = tk.Frame(main_frame)
        email_frame.pack(fill=tk.X, pady=(0, 25))
        
        # 邮箱标签
        email_label = tk.Label(
            email_frame,
            text="Email Address:",
            font=("Arial", 12, "bold"),
            fg="#2c3e50"
        )
        email_label.pack(anchor=tk.W, pady=(0, 8))
        
        # 邮箱输入框
        self.email_entry = tk.Entry(
            email_frame,
            font=("Arial", 13),
            width=35,
            relief=tk.SOLID,
            bd=2,
            bg="white",
            fg="#2c3e50"
        )
        self.email_entry.pack(fill=tk.X, pady=(0, 10))
        self.email_entry.focus()
        
        # 绑定回车键
        self.email_entry.bind('<Return>', lambda e: self.submit_email())
        
        # 示例文字
        example_label = tk.Label(
            email_frame,
            text="Example: user@example.com",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        example_label.pack(anchor=tk.W)
        
        # 按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 提交按钮
        submit_btn = tk.Button(
            button_frame,
            text="Submit",
            command=self.submit_email,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # 取消按钮
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_input,
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.LEFT)
    
    def validate_email(self, email):
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def submit_email(self):
        """提交邮箱"""
        email = self.email_entry.get().strip()
        
        if not email:
            messagebox.showerror("Error", "Please enter an email address")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        self.email = email
        self.root.destroy()
    
    def cancel_input(self):
        """取消输入"""
        self.email = None
        self.root.destroy()
    
    def get_email(self):
        """获取邮箱地址"""
        self.root.mainloop()
        return self.email

def get_email_input():
    """获取邮箱输入的便捷函数"""
    app = EmailInputGUI()
    return app.get_email()

if __name__ == "__main__":
    email = get_email_input()
    if email:
        print(f"Email entered: {email}")
    else:
        print("No email entered")
