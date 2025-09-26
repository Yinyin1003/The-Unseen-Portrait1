#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English Workflow - Complete Photo System
Integrates QR scanning, email input, head detection, and email sending
"""

import sys
import os
import time
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from back_detector import BackDetector
from email_sender import EmailSender
from config import EMAIL_CONFIG

class EnglishWorkflow:
    def __init__(self):
        self.detector = BackDetector()
        self.email_sender = EmailSender()
        self.captured_photos = []
        
    def simulate_qr_scan(self):
        """Simulate QR code scanning"""
        print("🔍 Scanning QR code...")
        time.sleep(1)
        print("✅ QR code scanned successfully!")
        return True
    
    def get_email_input(self):
        """Get email input from user"""
        print("\n📧 Please enter the recipient's email address:")
        print("(This will be used to send the captured photo)")
        
        # For demo purposes, use a pre-set email
        demo_email = "rebecca.zyy103@gmail.com"
        print(f"Demo email: {demo_email}")
        return demo_email
    
    def start_photo_session(self, recipient_email):
        """Start the photo detection session"""
        print(f"\n📸 Starting photo session for: {recipient_email}")
        print("Position yourself so your head is visible in the camera")
        print("The system will detect the back of your head and take a photo")
        print("Press ESC or Q to exit")
        
        try:
            self.detector.start_detection()
        except KeyboardInterrupt:
            print("\n⏹️ Photo session interrupted by user")
        except Exception as e:
            print(f"❌ Error during photo session: {str(e)}")
    
    def send_photo_email(self, recipient_email, photo_path):
        """Send the captured photo via email"""
        print(f"\n📤 Sending photo to: {recipient_email}")
        
        try:
            success = self.email_sender.send_photo(recipient_email, photo_path)
            if success:
                print("✅ Photo sent successfully!")
                print("Check the recipient's inbox for 'The Unseen Portrait'")
            else:
                print("❌ Failed to send photo")
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
    
    def run_complete_workflow(self):
        """Run the complete workflow"""
        print("=" * 60)
        print("🎭 The Unseen Portrait - Complete Workflow")
        print("=" * 60)
        
        try:
            # Step 1: QR Code Scanning
            print("\n📱 Step 1: QR Code Scanning")
            if not self.simulate_qr_scan():
                print("❌ QR code scanning failed")
                return
            
            # Step 2: Email Input
            print("\n📧 Step 2: Email Input")
            recipient_email = self.get_email_input()
            if not recipient_email:
                print("❌ No email provided")
                return
            
            # Step 3: Photo Detection
            print("\n📸 Step 3: Photo Detection")
            print("Starting camera...")
            time.sleep(2)
            
            # Start detection in a separate thread
            detection_thread = threading.Thread(target=self.start_photo_session, args=(recipient_email,))
            detection_thread.daemon = True
            detection_thread.start()
            
            # Wait for detection to complete or user interruption
            try:
                detection_thread.join()
            except KeyboardInterrupt:
                print("\n⏹️ Workflow interrupted by user")
                return
            
            # Step 4: Check for captured photos
            if hasattr(self.detector, 'last_photo_path') and self.detector.last_photo_path:
                print(f"\n📷 Photo captured: {self.detector.last_photo_path}")
                
                # Step 5: Send Email
                print("\n📤 Step 5: Sending Email")
                self.send_photo_email(recipient_email, self.detector.last_photo_path)
            else:
                print("❌ No photo was captured")
            
        except Exception as e:
            print(f"❌ Workflow error: {str(e)}")
        
        print("\n" + "=" * 60)
        print("🏁 Workflow completed!")
        print("=" * 60)

def main():
    """Main function"""
    print("Welcome to The Unseen Portrait System")
    print("This system will:")
    print("1. Scan a QR code")
    print("2. Get email input")
    print("3. Detect the back of your head")
    print("4. Take a photo")
    print("5. Send the photo via email")
    
    input("\nPress Enter to start the workflow...")
    
    workflow = EnglishWorkflow()
    workflow.run_complete_workflow()

if __name__ == "__main__":
    main()
