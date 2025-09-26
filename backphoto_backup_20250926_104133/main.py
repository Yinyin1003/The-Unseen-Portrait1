#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import threading
from datetime import datetime

# 导入自定义模块
from qr_scanner import QRScanner
from email_input import get_email_input
from back_detector import BackDetector
from email_sender import EmailSender

class AutoPhotoSystem:
    def __init__(self):
        self.qr_scanner = QRScanner()
        self.back_detector = BackDetector()
        self.email_sender = EmailSender()
        self.is_running = False
        self.current_email = None
        
    def print_banner(self):
        """打印系统横幅"""
        print("=" * 60)
        print("           自动拍照系统 v1.0")
        print("=" * 60)
        print("功能：扫描二维码 -> 输入邮箱 -> 自动拍照 -> 发送邮件")
        print("=" * 60)
    
    def print_menu(self):
        """打印菜单"""
        print("\n请选择操作：")
        print("1. 开始自动拍照流程")
        print("2. 测试二维码扫描")
        print("3. 测试邮箱输入")
        print("4. 测试后背检测")
        print("5. 测试邮件发送")
        print("6. 配置检查")
        print("0. 退出程序")
        print("-" * 40)
    
    def start_auto_photo_workflow(self):
        """开始自动拍照工作流程"""
        print("\n=== 开始自动拍照流程 ===")
        
        # 步骤1：扫描二维码
        print("\n步骤1：扫描二维码")
        print("请将二维码对准摄像头...")
        
        success, qr_data = self.qr_scanner.scan_qr_code()
        if not success:
            print("二维码扫描失败，流程终止")
            return False
        
        print(f"二维码扫描成功: {qr_data}")
        
        # 步骤2：输入邮箱
        print("\n步骤2：输入邮箱地址")
        result, email = get_email_input()
        if not result:
            print("邮箱输入取消，流程终止")
            return False
        
        self.current_email = email
        print(f"邮箱输入成功: {email}")
        
        # 步骤3：后背检测和拍照
        print("\n步骤3：后背检测和自动拍照")
        print("请坐在椅子上，系统将自动检测后背并拍照")
        print("按ESC键停止检测")
        
        def photo_callback(photo_path):
            """拍照回调函数"""
            print(f"\n照片已拍摄: {photo_path}")
            
            # 发送邮件
            print("正在发送邮件...")
            self.email_sender.send_photo_email_async(
                self.current_email, 
                photo_path,
                "这是系统为您自动拍摄的照片，请查收。",
                self.email_sent_callback
            )
        
        # 开始后背检测
        self.back_detector.start_detection(photo_callback)
        
        print("自动拍照流程完成")
        return True
    
    def email_sent_callback(self, success, email, photo_path):
        """邮件发送回调函数"""
        if success:
            print(f"✅ 照片已成功发送到: {email}")
        else:
            print(f"❌ 照片发送失败: {email}")
    
    def test_qr_scanner(self):
        """测试二维码扫描"""
        print("\n=== 测试二维码扫描 ===")
        success, data = self.qr_scanner.scan_qr_code(timeout=10)
        if success:
            print(f"✅ 二维码扫描测试成功: {data}")
        else:
            print("❌ 二维码扫描测试失败")
    
    def test_email_input(self):
        """测试邮箱输入"""
        print("\n=== 测试邮箱输入 ===")
        result, email = get_email_input()
        if result:
            print(f"✅ 邮箱输入测试成功: {email}")
        else:
            print("❌ 邮箱输入测试失败或取消")
    
    def test_back_detection(self):
        """测试后背检测"""
        print("\n=== 测试后背检测 ===")
        print("请坐在椅子上，系统将检测后背")
        print("按ESC键停止检测")
        
        def test_callback(photo_path):
            print(f"✅ 后背检测测试成功，照片已保存: {photo_path}")
        
        self.back_detector.start_detection(test_callback)
    
    def test_email_sending(self):
        """测试邮件发送"""
        print("\n=== 测试邮件发送 ===")
        
        # 先获取测试邮箱
        result, email = get_email_input()
        if not result:
            print("❌ 邮件发送测试取消")
            return
        
        # 测试连接
        if not self.email_sender.test_connection():
            print("❌ 邮件服务器连接失败，请检查配置")
            return
        
        # 发送测试邮件
        if self.email_sender.send_test_email(email):
            print(f"✅ 测试邮件发送成功: {email}")
        else:
            print("❌ 测试邮件发送失败")
    
    def check_configuration(self):
        """检查配置"""
        print("\n=== 配置检查 ===")
        
        # 检查摄像头
        print("检查摄像头...")
        if self.back_detector.start_camera():
            print("✅ 摄像头正常")
            self.back_detector.stop_detection()
        else:
            print("❌ 摄像头异常")
        
        # 检查邮件配置
        print("检查邮件配置...")
        if self.email_sender.test_connection():
            print("✅ 邮件服务器连接正常")
        else:
            print("❌ 邮件服务器连接失败")
        
        # 检查照片目录
        print("检查照片目录...")
        if not os.path.exists("photos"):
            os.makedirs("photos")
            print("✅ 照片目录已创建")
        else:
            print("✅ 照片目录已存在")
    
    def run(self):
        """运行主程序"""
        self.print_banner()
        
        while True:
            self.print_menu()
            
            try:
                choice = input("请输入选择 (0-6): ").strip()
                
                if choice == "0":
                    print("感谢使用自动拍照系统，再见！")
                    break
                elif choice == "1":
                    self.start_auto_photo_workflow()
                elif choice == "2":
                    self.test_qr_scanner()
                elif choice == "3":
                    self.test_email_input()
                elif choice == "4":
                    self.test_back_detection()
                elif choice == "5":
                    self.test_email_sending()
                elif choice == "6":
                    self.check_configuration()
                else:
                    print("无效选择，请重新输入")
                
                input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            except Exception as e:
                print(f"\n发生错误: {e}")
                input("按回车键继续...")
        
        # 清理资源
        self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        print("正在清理资源...")
        self.qr_scanner.stop_scanning()
        self.back_detector.stop_detection()
        print("资源清理完成")

def main():
    """主函数"""
    try:
        system = AutoPhotoSystem()
        system.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
