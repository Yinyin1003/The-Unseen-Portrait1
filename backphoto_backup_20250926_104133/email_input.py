import tkinter as tk
from tkinter import messagebox
import re
import threading

class EmailInputDialog:
    def __init__(self):
        self.email = None
        self.result = None
        self.window = None
        
    def validate_email(self, email):
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def on_submit(self):
        """提交邮箱"""
        email = self.email_entry.get().strip()
        
        if not email:
            messagebox.showerror("错误", "请输入邮箱地址")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("错误", "邮箱格式不正确")
            return
        
        self.email = email
        self.result = True
        self.window.destroy()
    
    def on_cancel(self):
        """取消输入"""
        self.result = False
        self.window.destroy()
    
    def show_dialog(self):
        """显示邮箱输入对话框"""
        self.window = tk.Tk()
        self.window.title("输入邮箱地址")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        
        # 居中显示
        self.window.eval('tk::PlaceWindow . center')
        
        # 主框架
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="请输入您的邮箱地址", 
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 说明文字
        info_label = tk.Label(
            main_frame,
            text="照片将发送到此邮箱",
            font=("Arial", 10),
            fg="gray"
        )
        info_label.pack(pady=(0, 10))
        
        # 邮箱输入框
        email_frame = tk.Frame(main_frame)
        email_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(email_frame, text="邮箱:", font=("Arial", 12)).pack(anchor=tk.W)
        
        self.email_entry = tk.Entry(
            email_frame, 
            font=("Arial", 12),
            width=30
        )
        self.email_entry.pack(fill=tk.X, pady=(5, 0))
        self.email_entry.focus()
        
        # 绑定回车键
        self.email_entry.bind('<Return>', lambda e: self.on_submit())
        
        # 按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # 提交按钮
        submit_btn = tk.Button(
            button_frame,
            text="确认",
            command=self.on_submit,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=10
        )
        submit_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 取消按钮
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=self.on_cancel,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=10
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # 设置窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # 运行对话框
        self.window.mainloop()
        
        return self.result, self.email

def get_email_input():
    """获取邮箱输入的便捷函数"""
    dialog = EmailInputDialog()
    return dialog.show_dialog()

# 测试函数
if __name__ == "__main__":
    result, email = get_email_input()
    if result:
        print(f"输入的邮箱: {email}")
    else:
        print("用户取消了输入")
