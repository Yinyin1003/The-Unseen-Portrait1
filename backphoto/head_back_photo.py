#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
后脑勺检测和拍照程序
专门用于识别后脑勺并自动拍照
"""

import sys
import os
import time
from datetime import datetime
from back_detector import BackDetector
from email_sender import EmailSender
from email_input import get_email_input

class HeadBackPhotoSystem:
    def __init__(self):
        self.detector = BackDetector()
        self.email_sender = EmailSender()
        self.photo_count = 0
        
    def print_banner(self):
        """打印系统横幅"""
        print("=" * 60)
        print("           后脑勺检测拍照系统 v1.0")
        print("=" * 60)
        print("功能：检测后脑勺 -> 自动拍照 -> 发送邮件")
        print("=" * 60)
    
    def start_head_detection(self, email=None):
        """
        开始后脑勺检测和拍照
        email: 如果提供邮箱，拍照后会自动发送邮件
        """
        print("\n=== 开始后脑勺检测 ===")
        print("请将后脑勺对准摄像头")
        print("系统将自动检测并拍照")
        print("按ESC键停止检测")
        
        def photo_callback(photo_path):
            """拍照回调函数"""
            self.photo_count += 1
            print(f"\n✅ 第 {self.photo_count} 张照片已拍摄: {photo_path}")
            
            if email:
                print("正在发送邮件...")
                self.email_sender.send_photo_email_async(
                    email, 
                    photo_path,
                    f"这是系统为您自动拍摄的第 {self.photo_count} 张后脑勺照片，请查收。",
                    self.email_sent_callback
                )
        
        # 开始检测
        try:
            self.detector.start_detection(photo_callback)
            print(f"\n检测完成，共拍摄了 {self.photo_count} 张照片")
        except Exception as e:
            print(f"检测过程中出错: {e}")
    
    def email_sent_callback(self, success, email, photo_path):
        """邮件发送回调函数"""
        if success:
            print(f"✅ 照片已成功发送到: {email}")
        else:
            print(f"❌ 照片发送失败: {email}")
    
    def test_detection(self):
        """测试检测功能"""
        print("\n=== 测试后脑勺检测功能 ===")
        print("请将后脑勺对准摄像头进行测试")
        
        def test_callback(photo_path):
            print(f"✅ 检测测试成功，照片已保存: {photo_path}")
        
        try:
            self.detector.start_detection(test_callback)
        except Exception as e:
            print(f"测试过程中出错: {e}")
    
    def check_system(self):
        """检查系统状态"""
        print("\n=== 系统状态检查 ===")
        
        # 检查摄像头
        print("1. 检查摄像头...")
        if self.detector.start_camera():
            print("✅ 摄像头正常")
            self.detector.stop_detection()
        else:
            print("❌ 摄像头异常")
        
        # 检查邮件配置
        print("2. 检查邮件配置...")
        if self.email_sender.test_connection():
            print("✅ 邮件服务器连接正常")
        else:
            print("❌ 邮件服务器连接失败")
        
        # 检查照片目录
        print("3. 检查照片目录...")
        if not os.path.exists("photos"):
            os.makedirs("photos")
            print("✅ 照片目录已创建")
        else:
            print("✅ 照片目录已存在")
        
        # 显示配置信息
        print("4. 当前配置:")
        print(f"   - 检测区域: 后脑勺区域")
        print(f"   - 拍照延迟: 2秒")
        print(f"   - 照片保存: photos/ 目录")
    
    def run(self):
        """运行主程序"""
        self.print_banner()
        
        while True:
            print("\n请选择操作：")
            print("1. 开始后脑勺检测和拍照")
            print("2. 检测并发送邮件")
            print("3. 测试检测功能")
            print("4. 系统状态检查")
            print("0. 退出程序")
            print("-" * 40)
            
            try:
                choice = input("请输入选择 (0-4): ").strip()
                
                if choice == "0":
                    print("感谢使用后脑勺检测拍照系统，再见！")
                    break
                elif choice == "1":
                    self.start_head_detection()
                elif choice == "2":
                    # 先获取邮箱
                    result, email = get_email_input()
                    if result:
                        self.start_head_detection(email)
                    else:
                        print("邮箱输入取消")
                elif choice == "3":
                    self.test_detection()
                elif choice == "4":
                    self.check_system()
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
        self.detector.stop_detection()
        print("资源清理完成")

def main():
    """主函数"""
    try:
        system = HeadBackPhotoSystem()
        system.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        print("\n请确保：")
        print("1. 已安装所有依赖: pip install -r requirements.txt")
        print("2. 摄像头权限已开启")
        print("3. 已正确配置邮件服务器（可选）")

if __name__ == "__main__":
    main()
