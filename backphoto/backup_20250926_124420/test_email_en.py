#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English Email Configuration Test
Tests email sending with the new English template
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_sender import EmailSender
from config import EMAIL_CONFIG

def test_email_configuration():
    """Test email configuration with English template"""
    print("=" * 50)
    print("Email Configuration Test (English)")
    print("=" * 50)
    
    # Display current configuration
    print("\nCurrent Email Configuration:")
    print(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}")
    print(f"SMTP Port: {EMAIL_CONFIG['smtp_port']}")
    print(f"Sender Email: {EMAIL_CONFIG['sender_email']}")
    print(f"Subject: {EMAIL_CONFIG['subject']}")
    print(f"Password: {'*' * len(EMAIL_CONFIG['sender_password'])}")
    
    # Test email sending
    print("\nTesting email sending...")
    
    try:
        sender = EmailSender()
        
        # Test with a sample email
        test_email = "rebecca.zyy103@gmail.com"  # Use the same email for testing
        print(f"Sending test email to: {test_email}")
        
        result = sender.send_test_email(test_email)
        
        if result:
            print("✅ Test email sent successfully!")
            print("Check your inbox for the email with subject 'The Unseen Portrait - Test'")
        else:
            print("❌ Failed to send test email")
            
    except Exception as e:
        print(f"❌ Error during email test: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your email configuration in config.py")
        print("2. For Gmail: Use App Password, not regular password")
        print("3. For QQ Mail: Use Authorization Code, not login password")
        print("4. Ensure 2FA is enabled for Gmail")
        print("5. Check your internet connection")

def show_configuration_guide():
    """Show configuration guide"""
    print("\n" + "=" * 50)
    print("Email Configuration Guide")
    print("=" * 50)
    
    print("\nFor Gmail:")
    print("1. Enable 2-Factor Authentication")
    print("2. Generate App Password (not regular password)")
    print("3. Update config.py with App Password")
    
    print("\nFor QQ Mail:")
    print("1. Enable SMTP service in QQ Mail settings")
    print("2. Generate Authorization Code")
    print("3. Update config.py with Authorization Code")
    
    print("\nCurrent config.py should look like:")
    print("EMAIL_CONFIG = {")
    print("    'smtp_server': 'smtp.gmail.com',")
    print("    'smtp_port': 587,")
    print("    'sender_email': 'your_email@gmail.com',")
    print("    'sender_password': 'your_app_password_here',")
    print("    'subject': 'The Unseen Portrait'")
    print("}")

if __name__ == "__main__":
    print("The Unseen Portrait - Email Configuration Test")
    print("This will test your email configuration with the new English template")
    
    # Test email configuration
    test_email_configuration()
    
    # Show configuration guide
    show_configuration_guide()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("If the test failed, please check your email configuration.")
    print("=" * 50)
