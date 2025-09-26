#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
邮件配置测试程序
帮助您测试和配置邮件服务器
"""

import sys
import os
from email_sender import EmailSender

def test_email_configuration():
    """测试邮件配置"""
    print("=" * 60)
    print("           邮件配置测试程序")
    print("=" * 60)
    
    sender = EmailSender()
    
    # 显示当前配置
    print("\n📧 当前邮件配置：")
    print(f"   SMTP服务器: {sender.smtp_server}")
    print(f"   端口: {sender.smtp_port}")
    print(f"   发送者邮箱: {sender.sender_email}")
    print(f"   密码: {'*' * len(sender.sender_password) if sender.sender_password else '未设置'}")
    
    # 测试连接
    print("\n🔍 测试邮件服务器连接...")
    if sender.test_connection():
        print("✅ 邮件服务器连接成功！")
        return True
    else:
        print("❌ 邮件服务器连接失败")
        print("\n请检查以下配置：")
        print("1. Gmail需要开启两步验证")
        print("2. 生成应用密码（不是登录密码）")
        print("3. 在 config.py 中正确设置邮箱和密码")
        return False

def test_email_sending():
    """测试邮件发送"""
    print("\n📤 测试邮件发送功能...")
    
    sender = EmailSender()
    
    # 获取测试邮箱
    print("请输入测试邮箱地址：")
    try:
        test_email = input("测试邮箱: ").strip()
        if not test_email:
            print("❌ 邮箱地址不能为空")
            return False
        
        if "@" not in test_email or "." not in test_email:
            print("❌ 邮箱格式不正确")
            return False
        
        print(f"正在向 {test_email} 发送测试邮件...")
        
        if sender.send_test_email(test_email):
            print("✅ 测试邮件发送成功！")
            print("请检查您的邮箱收件箱")
            return True
        else:
            print("❌ 测试邮件发送失败")
            return False
            
    except KeyboardInterrupt:
        print("\n❌ 测试取消")
        return False
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def show_configuration_guide():
    """显示配置指南"""
    print("\n📋 邮件配置指南：")
    print("=" * 40)
    
    print("\n🔧 Gmail配置步骤：")
    print("1. 登录Gmail账户")
    print("2. 进入 账户设置 → 安全性")
    print("3. 开启 两步验证")
    print("4. 生成 应用密码（16位）")
    print("5. 在 config.py 中设置：")
    print("   - sender_email: 您的Gmail邮箱")
    print("   - sender_password: 16位应用密码")
    
    print("\n🔧 QQ邮箱配置步骤：")
    print("1. 登录QQ邮箱")
    print("2. 进入 设置 → 账户")
    print("3. 开启 SMTP服务")
    print("4. 生成 授权码")
    print("5. 在 config.py 中设置：")
    print("   - smtp_server: 'smtp.qq.com'")
    print("   - smtp_port: 587")
    print("   - sender_email: 您的QQ邮箱")
    print("   - sender_password: 授权码")
    
    print("\n🔧 163邮箱配置步骤：")
    print("1. 登录163邮箱")
    print("2. 进入 设置 → POP3/SMTP/IMAP")
    print("3. 开启 SMTP服务")
    print("4. 生成 授权码")
    print("5. 在 config.py 中设置：")
    print("   - smtp_server: 'smtp.163.com'")
    print("   - smtp_port: 25")
    print("   - sender_email: 您的163邮箱")
    print("   - sender_password: 授权码")

def main():
    """主函数"""
    print("邮件配置测试程序")
    
    while True:
        print("\n请选择操作：")
        print("1. 测试邮件配置")
        print("2. 测试邮件发送")
        print("3. 显示配置指南")
        print("0. 退出")
        print("-" * 30)
        
        try:
            choice = input("请输入选择 (0-3): ").strip()
            
            if choice == "0":
                print("退出程序")
                break
            elif choice == "1":
                test_email_configuration()
            elif choice == "2":
                test_email_sending()
            elif choice == "3":
                show_configuration_guide()
            else:
                print("无效选择，请重新输入")
            
            input("\n按回车键继续...")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")
            input("按回车键继续...")

if __name__ == "__main__":
    main()
