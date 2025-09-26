#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def console_email_input():
    print("=" * 60)
    print("📧 邮箱输入程序")
    print("=" * 60)
    print()
    
    while True:
        try:
            email = input("请输入您的邮箱地址: ").strip()
            
            if not email:
                print("❌ 邮箱地址不能为空，请重新输入")
                continue
                
            if not validate_email(email):
                print("❌ 邮箱格式不正确，请重新输入 (例如: user@example.com)")
                continue
                
            print(f"✅ 邮箱格式正确: {email}")
            
            # 确认输入
            confirm = input("确认使用这个邮箱吗？(y/n): ").strip().lower()
            if confirm in ['y', 'yes', '是', '确认']:
                return email
            elif confirm in ['n', 'no', '否', '取消']:
                print("❌ 已取消输入")
                return None
            else:
                print("❌ 请输入 y 或 n")
                continue
                
        except KeyboardInterrupt:
            print("\n❌ 用户中断输入")
            return None
        except EOFError:
            print("\n❌ 输入结束")
            return None

if __name__ == "__main__":
    print("🚀 启动控制台邮箱输入程序...")
    
    email = console_email_input()
    
    print()
    print("=" * 60)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 60)
