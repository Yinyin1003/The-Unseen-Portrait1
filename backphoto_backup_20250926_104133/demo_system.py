#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动拍照系统演示版本
模拟完整的拍照流程，不需要实际摄像头
"""

import os
import time
from datetime import datetime
from email_sender import EmailSender
from email_input import get_email_input

class DemoPhotoSystem:
    def __init__(self):
        self.email_sender = EmailSender()
        
    def print_banner(self):
        """打印系统横幅"""
        print("=" * 60)
        print("           自动拍照系统 v1.0 (演示版)")
        print("=" * 60)
        print("功能：输入邮箱 -> 模拟拍照 -> 发送邮件")
        print("=" * 60)
    
    def create_demo_photo(self):
        """创建演示照片"""
        # 创建照片目录
        if not os.path.exists("photos"):
            os.makedirs("photos")
        
        # 创建一个简单的演示照片文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photos/demo_photo_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("自动拍照系统演示照片\n")
            f.write(f"拍摄时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
            f.write("这是一个演示照片文件\n")
            f.write("在实际使用中，这里会是一张真实的照片\n")
        
        return filename
    
    def start_demo_workflow(self):
        """开始演示工作流程"""
        print("\n=== 开始自动拍照演示流程 ===")
        
        # 步骤1：输入邮箱
        print("\n步骤1：输入邮箱地址")
        result, email = get_email_input()
        if not result:
            print("邮箱输入取消，流程终止")
            return False
        
        print(f"邮箱输入成功: {email}")
        
        # 步骤2：模拟后背检测
        print("\n步骤2：模拟后背检测")
        print("正在检测后背...")
        for i in range(3):
            print(f"检测中... {i+1}/3")
            time.sleep(1)
        
        print("✅ 检测到后背！")
        
        # 步骤3：模拟拍照
        print("\n步骤3：模拟拍照")
        print("正在拍照...")
        time.sleep(2)
        
        photo_path = self.create_demo_photo()
        print(f"✅ 照片已拍摄: {photo_path}")
        
        # 步骤4：发送邮件
        print("\n步骤4：发送邮件")
        print("正在发送邮件...")
        
        try:
            if self.email_sender.send_photo_email(email, photo_path, "这是系统演示拍摄的照片，请查收。"):
                print(f"✅ 照片已成功发送到: {email}")
                print("请检查您的邮箱收件箱")
            else:
                print(f"❌ 照片发送失败: {email}")
                print("请检查邮件配置")
        except Exception as e:
            print(f"❌ 发送邮件时出错: {e}")
        
        print("\n演示流程完成！")
        return True
    
    def test_email_only(self):
        """仅测试邮件功能"""
        print("\n=== 测试邮件功能 ===")
        
        result, email = get_email_input()
        if not result:
            print("邮箱输入取消")
            return
        
        print(f"正在向 {email} 发送测试邮件...")
        
        if self.email_sender.send_test_email(email):
            print("✅ 测试邮件发送成功！")
        else:
            print("❌ 测试邮件发送失败")
    
    def run(self):
        """运行演示系统"""
        self.print_banner()
        
        while True:
            print("\n请选择操作：")
            print("1. 开始演示流程")
            print("2. 测试邮件功能")
            print("0. 退出")
            print("-" * 30)
            
            try:
                choice = input("请输入选择 (0-2): ").strip()
                
                if choice == "0":
                    print("感谢使用自动拍照系统，再见！")
                    break
                elif choice == "1":
                    self.start_demo_workflow()
                elif choice == "2":
                    self.test_email_only()
                else:
                    print("无效选择，请重新输入")
                
                input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            except Exception as e:
                print(f"\n发生错误: {e}")
                input("按回车键继续...")

def main():
    """主函数"""
    try:
        system = DemoPhotoSystem()
        system.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        print("\n请确保：")
        print("1. 已安装所有依赖: pip install -r requirements.txt")
        print("2. 已正确配置邮件服务器")

if __name__ == "__main__":
    main()
