#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复的工作流程：扫码 → 输入邮箱 → 拍照 → 发送邮件
使用终端直接输入邮箱地址
"""

import sys
import os
import time
from datetime import datetime
from back_detector import BackDetector
from email_sender import EmailSender

class FixedWorkflow:
    def __init__(self):
        self.detector = BackDetector()
        self.email_sender = EmailSender()
        self.current_email = None
        self.photo_count = 0
        
    def print_banner(self):
        """打印系统横幅"""
        print("=" * 70)
        print("           修复的工作流程：扫码 → 邮箱 → 拍照 → 发送邮件")
        print("=" * 70)
        print("步骤：")
        print("1. 扫描二维码（模拟）")
        print("2. 输入邮箱地址（终端输入）")
        print("3. 检测后脑勺并拍照")
        print("4. 自动发送照片到邮箱")
        print("=" * 70)
    
    def step1_scan_qr_code(self):
        """步骤1：扫描二维码（模拟）"""
        print("\n📱 步骤1：扫描二维码")
        print("正在扫描二维码...")
        time.sleep(2)  # 模拟扫描时间
        
        # 模拟二维码扫描成功
        qr_data = "backphoto_system"
        print(f"✅ 二维码扫描成功: {qr_data}")
        return True
    
    def step2_input_email(self):
        """步骤2：输入邮箱地址"""
        print("\n📧 步骤2：输入邮箱地址")
        print("请在下方输入您的邮箱地址：")
        
        # 提供一些示例邮箱
        print("示例：your_email@gmail.com")
        print("按回车键确认输入")
        
        try:
            email = input("邮箱地址: ").strip()
            if not email:
                print("❌ 邮箱地址不能为空")
                return False
            
            # 简单的邮箱格式验证
            if "@" not in email or "." not in email:
                print("❌ 邮箱格式不正确，请重新输入")
                return False
            
            self.current_email = email
            print(f"✅ 邮箱输入成功: {email}")
            return True
        except KeyboardInterrupt:
            print("\n❌ 邮箱输入取消，流程终止")
            return False
        except Exception as e:
            print(f"❌ 邮箱输入出错: {e}")
            return False
    
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

def main():
    """主函数"""
    try:
        workflow = FixedWorkflow()
        workflow.run_complete_workflow()
    except Exception as e:
        print(f"程序启动失败: {e}")
        print("\n请确保：")
        print("1. 已安装所有依赖: pip install -r requirements.txt")
        print("2. 摄像头权限已开启")
        print("3. 已正确配置邮件服务器")

if __name__ == "__main__":
    main()
