#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run with Config Email
Uses email from user_email_config.py
"""

import sys
import os
import time
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from back_detector import BackDetector
from email_sender import EmailSender
from user_email_config import USER_EMAIL_CONFIG
from config import EMAIL_CONFIG

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
    print("• Use email from user_email_config.py")
    print("• Detect the back of your head")
    print("• Take a photo")
    print("• Send the photo via email with your custom message")
    
    # 从配置文件获取邮箱
    recipient_email = USER_EMAIL_CONFIG['recipient_email']
    auto_send = USER_EMAIL_CONFIG['auto_send']
    
    print(f"\n📧 Email will be sent to: {recipient_email}")
    print(f"📤 Auto-send enabled: {auto_send}")
    
    if not auto_send:
        print("❌ Auto-send is disabled in user_email_config.py")
        return
    
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
