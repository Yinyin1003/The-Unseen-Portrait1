#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import re

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

class EmailInputApp:
    def __init__(self, root):
        self.root = root
        self.email = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面 - Tkinter Designer风格"""
        # 窗口设置
        self.root.title("邮箱输入 - Designer版本")
        self.root.geometry("600x450+150+150")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        
        # 创建主容器
        self.main_container = tk.Frame(self.root, bg="#f0f0f0")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题区域
        self.title_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        self.title_label = tk.Label(
            self.title_frame,
            text="📧 邮箱输入",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        self.title_label.pack()
        
        # 说明区域
        self.info_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        self.info_frame.pack(fill="x", pady=(0, 30))
        
        self.info_label = tk.Label(
            self.info_frame,
            text="请输入您的邮箱地址，我们将用于发送处理结果",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        self.info_label.pack()
        
        # 输入区域
        self.input_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        self.input_frame.pack(fill="x", pady=(0, 30))
        
        # 输入框标签
        self.input_label = tk.Label(
            self.input_frame,
            text="邮箱地址：",
            font=("Arial", 12, "bold"),
            fg="#34495e",
            bg="#f0f0f0"
        )
        self.input_label.pack(anchor="w", pady=(0, 5))
        
        # 输入框容器
        self.entry_container = tk.Frame(self.input_frame, bg="#f0f0f0")
        self.entry_container.pack(fill="x")
        
        # 输入框
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(
            self.entry_container,
            textvariable=self.email_var,
            font=("Arial", 14),
            relief="solid",
            bd=2,
            bg="white",
            fg="#2c3e50",
            insertbackground="#2c3e50"
        )
        self.email_entry.pack(fill="x", ipady=10)
        self.email_entry.bind('<Return>', self.submit_email)
        self.email_entry.focus()
        
        # 占位符效果
        self.placeholder_text = "例如: user@example.com"
        self.email_entry.insert(0, self.placeholder_text)
        self.email_entry.configure(fg="#95a5a6")
        
        def on_focus_in(event):
            if self.email_entry.get() == self.placeholder_text:
                self.email_entry.delete(0, tk.END)
                self.email_entry.configure(fg="#2c3e50")
        
        def on_focus_out(event):
            if not self.email_entry.get():
                self.email_entry.insert(0, self.placeholder_text)
                self.email_entry.configure(fg="#95a5a6")
        
        self.email_entry.bind('<FocusIn>', on_focus_in)
        self.email_entry.bind('<FocusOut>', on_focus_out)
        
        # 按钮区域
        self.button_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        self.button_frame.pack(fill="x", pady=(0, 20))
        
        # 按钮容器
        self.btn_container = tk.Frame(self.button_frame, bg="#f0f0f0")
        self.btn_container.pack()
        
        # 确认按钮
        self.submit_btn = tk.Button(
            self.btn_container,
            text="确认",
            command=self.submit_email,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2"
        )
        self.submit_btn.pack(side="left", padx=(0, 15))
        
        # 取消按钮
        self.cancel_btn = tk.Button(
            self.btn_container,
            text="取消",
            command=self.cancel_input,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2"
        )
        self.cancel_btn.pack(side="left")
        
        # 底部信息
        self.bottom_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        self.bottom_frame.pack(fill="x", side="bottom")
        
        self.bottom_label = tk.Label(
            self.bottom_frame,
            text="您的邮箱信息将被安全保存，仅用于发送处理结果",
            font=("Arial", 10),
            fg="#95a5a6",
            bg="#f0f0f0"
        )
        self.bottom_label.pack()
        
        # 按钮悬停效果
        self.setup_hover_effects()
    
    def setup_hover_effects(self):
        """设置按钮悬停效果"""
        def on_enter_submit(event):
            self.submit_btn.configure(bg="#229954")
        
        def on_leave_submit(event):
            self.submit_btn.configure(bg="#27ae60")
        
        def on_enter_cancel(event):
            self.cancel_btn.configure(bg="#c0392b")
        
        def on_leave_cancel(event):
            self.cancel_btn.configure(bg="#e74c3c")
        
        self.submit_btn.bind("<Enter>", on_enter_submit)
        self.submit_btn.bind("<Leave>", on_leave_submit)
        self.cancel_btn.bind("<Enter>", on_enter_cancel)
        self.cancel_btn.bind("<Leave>", on_leave_cancel)
    
    def submit_email(self, event=None):
        """提交邮箱"""
        email = self.email_var.get().strip()
        
        # 处理占位符
        if email == self.placeholder_text:
            email = ""
        
        if not email:
            messagebox.showerror("错误", "请输入邮箱地址")
            return
        
        if not validate_email(email):
            messagebox.showerror("错误", "请输入有效的邮箱地址")
            return
        
        self.email = email
        print(f"✅ 用户输入邮箱: {email}")
        self.root.destroy()
    
    def cancel_input(self):
        """取消输入"""
        print("❌ 用户取消输入")
        self.root.destroy()

def designer_email_input():
    """使用Tkinter Designer风格创建邮箱输入界面"""
    print("🚀 启动Designer邮箱输入窗口...")
    
    root = tk.Tk()
    app = EmailInputApp(root)
    
    # 强制显示
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    
    print("📱 Designer窗口应该已经显示...")
    
    root.mainloop()
    return app.email

if __name__ == "__main__":
    print("=" * 50)
    print("开始运行Designer邮箱输入程序")
    print("=" * 50)
    
    email = designer_email_input()
    
    print("=" * 50)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 50)
