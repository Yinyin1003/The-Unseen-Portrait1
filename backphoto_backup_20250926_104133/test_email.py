#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
邮件功能测试脚本
测试邮件发送功能是否正常工作
"""

from email_sender import EmailSender
from email_input import get_email_input

def test_email_configuration():
    """测试邮件配置"""
    print("=" * 50)
    print("           邮件配置测试")
    print("=" * 50)
    
    sender = EmailSender()
    
    # 测试连接
    print("\n1. 测试邮件服务器连接...")
    if sender.test_connection():
        print("✅ 邮件服务器连接成功")
        return True
    else:
        print("❌ 邮件服务器连接失败")
        print("请检查 config.py 中的邮件配置")
        return False

def test_email_sending():
    """测试邮件发送"""
    print("\n2. 测试邮件发送功能...")
    print("请输入测试邮箱地址：")
    
    try:
        result, email = get_email_input()
        if not result:
            print("❌ 邮箱输入取消")
            return False
        
        print(f"正在向 {email} 发送测试邮件...")
        
        sender = EmailSender()
        if sender.send_test_email(email):
            print("✅ 测试邮件发送成功！")
            print("请检查您的邮箱收件箱")
            return True
        else:
            print("❌ 测试邮件发送失败")
            return False
            
    except Exception as e:
        print(f"❌ 邮件发送出错: {e}")
        return False

def main():
    """主函数"""
    print("自动拍照系统 - 邮件功能测试")
    
    # 测试邮件配置
    if not test_email_configuration():
        print("\n请检查以下配置：")
        print("1. Gmail需要开启两步验证")
        print("2. 生成应用密码（不是登录密码）")
        print("3. 在 config.py 中正确设置邮箱和密码")
        return
    
    # 测试邮件发送
    if test_email_sending():
        print("\n🎉 邮件功能测试成功！")
        print("系统已准备就绪，可以开始使用自动拍照功能")
    else:
        print("\n❌ 邮件功能测试失败")
        print("请检查网络连接和邮件配置")

if __name__ == "__main__":
    main()
