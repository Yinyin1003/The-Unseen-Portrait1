#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import simpledialog, messagebox
import sys

def native_email_input():
    print("🚀 启动原生邮箱输入对话框...")
    
    # 创建隐藏的主窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    try:
        # 使用系统原生的输入对话框
        email = simpledialog.askstring(
            "邮箱输入", 
            "请输入您的邮箱地址：",
            parent=root
        )
        
        if email:
            print(f"✅ 用户输入邮箱: {email}")
            return email
        else:
            print("❌ 用户取消输入")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None
    finally:
        root.destroy()

if __name__ == "__main__":
    print("=" * 50)
    print("开始运行原生邮箱输入程序")
    print("=" * 50)
    
    email = native_email_input()
    
    print("=" * 50)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 50)
