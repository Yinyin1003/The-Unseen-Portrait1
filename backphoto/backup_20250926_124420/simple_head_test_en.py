#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English Simple Head Detection Test
Tests head detection with English interface
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from back_detector import BackDetector

def main():
    """Main function for head detection test"""
    print("=" * 50)
    print("🎭 The Unseen Portrait - Head Detection Test")
    print("=" * 50)
    print("This program will detect the back of your head and take photos")
    print("Features:")
    print("• Only captures the back of the head (no frontal face)")
    print("• Sound notification when photo is taken")
    print("• Anti-duplication (one photo per head)")
    print("• Visual feedback and status display")
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
        
        detector.start_detection()
        
    except KeyboardInterrupt:
        print("\n⏹️ Program interrupted by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check camera permissions")
        print("2. Ensure camera is not being used by other applications")
        print("3. Try running from terminal instead of IDE")
    
    print("\n" + "=" * 50)
    print("🏁 Head detection test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
