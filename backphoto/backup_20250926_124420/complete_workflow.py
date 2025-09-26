#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整工作流程：扫码 → 输入邮箱 → 拍照 → 发送邮件
"""

import sys
import os
import time
from datetime import datetime
from back_detector import BackDetector
from email_sender import EmailSender
from email_input import get_email_input

class CompleteWorkflow:
    def __init__(self):
        self.detector = BackDetector()
        self.email_sender = EmailSender()
        self.current_email = None
        self.photo_count = 0
        
    def print_banner(self):
        """打印系统横幅"""
        print("=" * 70)
        print("           完整工作流程：扫码 → 邮箱 → 拍照 → 发送邮件")
        print("=" * 70)
        print("步骤：")
        print("1. 扫描二维码")
        print("2. 输入邮箱地址")
        print("3. 检测后脑勺并拍照")
        print("4. 自动发送照片到邮箱")
        print("=" * 70)
    
    def step1_scan_qr_code(self):
        """步骤1：扫描二维码"""
        print("\n📱 步骤1：扫描二维码")
        print("请将二维码对准摄像头...")
        
        # 模拟二维码扫描（实际项目中可以集成真实的二维码扫描）
        print("正在扫描二维码...")
        time.sleep(2)  # 模拟扫描时间
        
        # 这里可以集成真实的二维码扫描功能
        # 暂时使用模拟数据
        qr_data = "backphoto_system"
        print(f"✅ 二维码扫描成功: {qr_data}")
        return True
    
    def step2_input_email(self):
        """步骤2：输入邮箱地址"""
        print("\n📧 步骤2：输入邮箱地址")
        print("请在弹出窗口中输入您的邮箱地址")
        
        result, email = get_email_input()
        if not result:
            print("❌ 邮箱输入取消，流程终止")
            return False
        
        self.current_email = email
        print(f"✅ 邮箱输入成功: {email}")
        return True
    
    def step3_detect_and_photo(self):
        """步骤3：检测后脑勺并拍照"""
        print("\n📸 步骤3：检测后脑勺并拍照")
        print("请将后脑勺对准摄像头")
        print("系统将自动检测并拍照")
        print("按ESC键停止检测")
        
        def photo_callback(photo_path):
            """拍照回调函数"""
            self.photo_count += 1
            print(f"📸 第 {self.photo_count} 张后脑勺照片已拍摄: {photo_path}")
            
            # 自动发送邮件
            if self.current_email:
                print(f"📤 正在发送照片到: {self.current_email}")
                self.email_sender.send_photo_email_async(
                    self.current_email, 
                    photo_path,
                    f"这是系统为您自动拍摄的第 {self.photo_count} 张后脑勺照片，请查收。",
                    self.email_sent_callback
                )
        
        try:
            self.detector.start_detection(photo_callback)
            print(f"\n✅ 检测完成，共拍摄了 {self.photo_count} 张照片")
            return True
        except Exception as e:
            print(f"❌ 检测过程中出错: {e}")
            return False
    
    def email_sent_callback(self, success, email, photo_path):
        """邮件发送回调函数"""
        if success:
            print(f"✅ 照片已成功发送到: {email}")
        else:
            print(f"❌ 照片发送失败: {email}")
    
    def run_complete_workflow(self):
        """运行完整工作流程"""
        self.print_banner()
        
        try:
            # 步骤1：扫描二维码
            if not self.step1_scan_qr_code():
                return False
            
            # 步骤2：输入邮箱
            if not self.step2_input_email():
                return False
            
            # 步骤3：检测并拍照
            if not self.step3_detect_and_photo():
                return False
            
            print("\n🎉 完整工作流程执行成功！")
            print(f"📊 统计结果：")
            print(f"   - 共拍摄了 {self.photo_count} 张后脑勺照片")
            print(f"   - 照片已发送到: {self.current_email}")
            return True
            
        except KeyboardInterrupt:
            print("\n🛑 用户中断流程")
            return False
        except Exception as e:
            print(f"\n❌ 流程执行出错: {e}")
            return False
        finally:
            self.detector.stop_detection()
    
    def run(self):
        """运行主程序"""
        while True:
            print("\n请选择操作：")
            print("1. 开始完整工作流程")
            print("2. 测试邮箱输入")
            print("3. 测试邮件发送")
            print("4. 系统状态检查")
            print("0. 退出程序")
            print("-" * 40)
            
            try:
                choice = input("请输入选择 (0-4): ").strip()
                
                if choice == "0":
                    print("感谢使用完整工作流程系统，再见！")
                    break
                elif choice == "1":
                    self.run_complete_workflow()
                elif choice == "2":
                    self.test_email_input()
                elif choice == "3":
                    self.test_email_sending()
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
    
    def test_email_input(self):
        """测试邮箱输入"""
        print("\n=== 测试邮箱输入 ===")
        result, email = get_email_input()
        if result:
            print(f"✅ 邮箱输入测试成功: {email}")
        else:
            print("❌ 邮箱输入测试失败或取消")
    
    def test_email_sending(self):
        """测试邮件发送"""
        print("\n=== 测试邮件发送 ===")
        result, email = get_email_input()
        if not result:
            print("❌ 邮件发送测试取消")
            return
        
        if self.email_sender.send_test_email(email):
            print(f"✅ 测试邮件发送成功: {email}")
        else:
            print("❌ 测试邮件发送失败")
    
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

def main():
    """主函数"""
    try:
        workflow = CompleteWorkflow()
        workflow.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        print("\n请确保：")
        print("1. 已安装所有依赖: pip install -r requirements.txt")
        print("2. 摄像头权限已开启")
        print("3. 已正确配置邮件服务器")

if __name__ == "__main__":
    main()
