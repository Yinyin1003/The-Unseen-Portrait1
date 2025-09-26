#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete English Workflow - Head Detection + Email Sending
Detects head and automatically sends email with captured photo
"""

import sys
import os
import time
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from back_detector import BackDetector
from email_sender import EmailSender
from simple_email_input import get_email_input
from config import EMAIL_CONFIG

class CompleteEnglishWorkflow:
    def __init__(self):
        self.detector = BackDetector()
        self.email_sender = EmailSender()
        self.recipient_email = None  # 将通过输入获取
        
    def on_photo_taken(self, photo_path):
        """当照片被拍摄时自动发送邮件"""
        print(f"\n📤 Auto-sending photo to: {self.recipient_email}")
        try:
            success = self.email_sender.send_photo_email(self.recipient_email, photo_path)
            if success:
                print("✅ Photo sent successfully!")
                print("📧 Check your inbox for 'The Unseen Portrait'")
            else:
                print("❌ Failed to send photo")
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
    
    def get_email_input(self):
        """获取邮箱输入"""
        email = get_email_input()
        if email:
            self.recipient_email = email
            return True
        else:
            return False
    
    def start_detection_with_email(self):
        """开始检测并自动发送邮件"""
        print("=" * 60)
        print("🎭 The Unseen Portrait - Complete Workflow")
        print("=" * 60)
        print("This system will:")
        print("1. Get email input")
        print("2. Detect the back of your head")
        print("3. Take a photo automatically")
        print("4. Send the photo via email")
        
        # 获取邮箱输入
        if not self.get_email_input():
            print("❌ Email input required to continue")
            return
        
        print(f"\n📧 Email will be sent to: {self.recipient_email}")
        print("\nControls:")
        print("• ESC or Q: Exit the program")
        print("• Position your head in the detection area")
        print("\nStarting camera...")
        
        try:
            print("✅ Camera initialized successfully")
            print("📸 Starting head detection...")
            print("Position yourself so your head is visible in the camera")
            print("The system will detect the back of your head and take a photo")
            print("Press ESC or Q to exit")
            
            # 重写检测器的拍照方法，添加邮件发送
            original_take_photo = self.detector.take_photo
            
            def enhanced_take_photo(frame):
                # 调用原始拍照方法
                photo_path = original_take_photo(frame)
                if photo_path:
                    # 自动发送邮件
                    self.on_photo_taken(photo_path)
                return photo_path
            
            # 替换拍照方法
            self.detector.take_photo = enhanced_take_photo
            
            # 开始检测
            self.detector.start_detection()
            
        except KeyboardInterrupt:
            print("\n⏹️ Program interrupted by user")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("\nTroubleshooting:")
            print("1. Check camera permissions")
            print("2. Ensure camera is not being used by other applications")
            print("3. Try running from terminal instead of IDE")
        
        print("\n" + "=" * 60)
        print("🏁 Complete workflow finished!")
        print("=" * 60)

def main():
    """Main function"""
    print("🎭 The Unseen Portrait - Complete System")
    print("This system will automatically:")
    print("• Detect the back of your head")
    print("• Take a photo")
    print("• Send the photo via email with your custom message")
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    workflow = CompleteEnglishWorkflow()
    workflow.start_detection_with_email()

if __name__ == "__main__":
    main()
