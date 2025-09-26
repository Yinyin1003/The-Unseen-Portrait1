#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run with Email Input
Simple version that allows email input in terminal
"""

import sys
import os
import time
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from back_detector import BackDetector
from email_sender import EmailSender
from config import EMAIL_CONFIG

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
            
            if "@" not in email or "." not in email:
                print("❌ Please enter a valid email address (e.g., user@example.com)")
                continue
            
            print(f"✅ Email set to: {email}")
            return email
            
        except KeyboardInterrupt:
            print("\n⏹️ Email input cancelled")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None

def on_photo_taken(photo_path, recipient_email):
    """当照片被拍摄时自动发送邮件"""
    print(f"\n📤 Auto-sending photo to: {recipient_email}")
    try:
        sender = EmailSender()
        success = sender.send_photo_email(recipient_email, photo_path)
        if success:
            print("✅ Photo sent successfully!")
            print("📧 Check your inbox for 'The Unseen Portrait'")
        else:
            print("❌ Failed to send photo")
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")

def main():
    """Main function"""
    print("🎭 The Unseen Portrait - Complete System")
    print("This system will automatically:")
    print("• Get email input")
    print("• Detect the back of your head")
    print("• Take a photo")
    print("• Send the photo via email with your custom message")
    
    # 获取邮箱输入
    recipient_email = get_email_input()
    if not recipient_email:
        print("❌ Email input required to continue")
        return
    
    print(f"\n📧 Email will be sent to: {recipient_email}")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    print("=" * 60)
    print("🎭 The Unseen Portrait - Complete Workflow")
    print("=" * 60)
    print("This system will:")
    print("1. Detect the back of your head")
    print("2. Take a photo automatically")
    print("3. Send the photo via email")
    
    print("\nControls:")
    print("• ESC or Q: Exit the program")
    print("• Position your head in the detection area")
    print("\nStarting camera...")
    
    try:
        detector = BackDetector()
        print("✅ Camera initialized successfully")
        print("📸 Starting head detection...")
        print("Position yourself so your head is visible in the camera")
        print("The system will detect the back of your head and take a photo")
        print("Press ESC or Q to exit")
        
        # 重写检测器的拍照方法，添加邮件发送
        original_take_photo = detector.take_photo
        
        def enhanced_take_photo(frame):
            # 调用原始拍照方法
            photo_path = original_take_photo(frame)
            if photo_path:
                # 自动发送邮件
                on_photo_taken(photo_path, recipient_email)
            return photo_path
        
        # 替换拍照方法
        detector.take_photo = enhanced_take_photo
        
        # 开始检测
        detector.start_detection()
        
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

if __name__ == "__main__":
    main()
