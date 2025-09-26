#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试GUI显示
"""

import tkinter as tk
from tkinter import messagebox
import sys

def test_gui():
    print("正在创建GUI窗口...")
    
    root = tk.Tk()
    root.title("测试窗口")
    
    # 设置窗口大小和位置
    root.geometry("500x400+100+100")
    
    # 设置背景色
    root.configure(bg="lightblue")
    
    # 添加一个大的标签
    label = tk.Label(root, text="这是一个测试窗口\n如果您能看到这个窗口，说明GUI工作正常", 
                    font=("Arial", 16), bg="lightblue", fg="darkblue")
    label.pack(expand=True)
    
    # 添加按钮
    def on_click():
        messagebox.showinfo("成功", "按钮点击成功！")
        root.destroy()
    
    button = tk.Button(root, text="点击测试", command=on_click, 
                      font=("Arial", 14), bg="green", fg="white", padx=20, pady=10)
    button.pack(pady=20)
    
    print("GUI窗口已创建，请查看屏幕...")
    
    # 确保窗口可见
    root.lift()
    root.focus_force()
    
    root.mainloop()
    print("GUI窗口已关闭")

if __name__ == "__main__":
    print("开始测试GUI...")
    test_gui()
    print("测试完成")
