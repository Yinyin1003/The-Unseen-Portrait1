#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_email():
    """获取邮箱地址"""
    # 预设邮箱地址
    default_email = "rebecca.zyy103@gmail.com"
    
    print("=" * 60)
    print("📧 邮箱输入程序")
    print("=" * 60)
    print(f"默认邮箱: {default_email}")
    print()
    
    # 验证默认邮箱
    if validate_email(default_email):
        print(f"✅ 使用默认邮箱: {default_email}")
        return default_email
    else:
        print("❌ 默认邮箱格式不正确")
        return None

if __name__ == "__main__":
    print("🚀 启动邮箱程序...")
    
    email = get_email()
    
    print()
    print("=" * 60)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 60)
