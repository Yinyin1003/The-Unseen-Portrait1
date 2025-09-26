#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统测试脚本
自动运行配置检查和基本功能测试
"""

import sys
import os
from email_input import get_email_input
from back_detector import BackDetector
from email_sender import EmailSender

def test_configuration():
    """测试系统配置"""
    print("=" * 50)
    print("           系统配置检查")
    print("=" * 50)
    
    # 检查摄像头
    print("\n1. 检查摄像头...")
    detector = BackDetector()
    if detector.start_camera():
        print("✅ 摄像头正常")
        detector.stop_detection()
    else:
        print("❌ 摄像头异常")
    
    # 检查邮件配置
    print("\n2. 检查邮件配置...")
    sender = EmailSender()
    if sender.test_connection():
        print("✅ 邮件服务器连接正常")
    else:
        print("❌ 邮件服务器连接失败")
        print("请检查 config.py 中的邮件配置")
    
    # 检查照片目录
    print("\n3. 检查照片目录...")
    if not os.path.exists("photos"):
        os.makedirs("photos")
        print("✅ 照片目录已创建")
    else:
        print("✅ 照片目录已存在")
    
    print("\n" + "=" * 50)

def test_email_input():
    """测试邮箱输入功能"""
    print("\n测试邮箱输入功能...")
    print("请在弹出窗口中输入测试邮箱地址")
    
    try:
        result, email = get_email_input()
        if result:
            print(f"✅ 邮箱输入测试成功: {email}")
            return email
        else:
            print("❌ 邮箱输入测试失败或取消")
            return None
    except Exception as e:
        print(f"❌ 邮箱输入测试出错: {e}")
        return None

def test_email_sending(email):
    """测试邮件发送功能"""
    if not email:
        print("跳过邮件发送测试（没有邮箱地址）")
        return
    
    print(f"\n测试邮件发送功能到: {email}")
    sender = EmailSender()
    
    if sender.send_test_email(email):
        print("✅ 测试邮件发送成功")
    else:
        print("❌ 测试邮件发送失败")

def test_back_detection():
    """测试后背检测功能"""
    print("\n测试后背检测功能...")
    print("请坐在椅子上，系统将检测后背")
    print("按ESC键停止检测")
    
    detector = BackDetector()
    
    def test_callback(photo_path):
        print(f"✅ 后背检测测试成功，照片已保存: {photo_path}")
    
    try:
        detector.start_detection(test_callback)
    except Exception as e:
        print(f"❌ 后背检测测试出错: {e}")

def main():
    """主测试函数"""
    print("自动拍照系统 - 功能测试")
    
    # 1. 配置检查
    test_configuration()
    
    # 2. 邮箱输入测试
    test_email = test_email_input()
    
    # 3. 邮件发送测试
    test_email_sending(test_email)
    
    # 4. 后背检测测试
    print("\n是否要测试后背检测功能？(y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice == 'y' or choice == 'yes':
            test_back_detection()
        else:
            print("跳过后背检测测试")
    except:
        print("跳过后背检测测试")
    
    print("\n测试完成！")
    print("\n使用说明：")
    print("1. 运行 'python3 simple_main.py' 启动完整系统")
    print("2. 选择 '1' 开始自动拍照流程")
    print("3. 输入邮箱地址")
    print("4. 坐在椅子上等待自动拍照")
    print("5. 照片会自动发送到指定邮箱")

if __name__ == "__main__":
    main()
