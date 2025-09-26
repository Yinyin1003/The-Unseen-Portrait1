#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Email Input
Terminal-based email input with validation
"""

import re
import sys

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_email_input():
    """获取邮箱输入"""
    print("=" * 50)
    print("🎭 The Unseen Portrait - Email Input")
    print("=" * 50)
    print("Please enter the recipient's email address:")
    print("(This will be used to send the captured photo)")
    print()
    
    while True:
        try:
            email = input("📧 Email: ").strip()
            
            if not email:
                print("❌ Please enter an email address")
                continue
            
            if not validate_email(email):
                print("❌ Please enter a valid email address (e.g., user@example.com)")
                continue
            
            print(f"✅ Email set to: {email}")
            return email
            
        except KeyboardInterrupt:
            print("\n⏹️ Email input cancelled")
            return None
        except EOFError:
            print("\n⏹️ Email input cancelled")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None

def main():
    """测试函数"""
    email = get_email_input()
    if email:
        print(f"\n✅ Email entered: {email}")
    else:
        print("\n❌ No email entered")

if __name__ == "__main__":
    main()
