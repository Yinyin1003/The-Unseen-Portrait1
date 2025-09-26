#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
后脑勺检测测试程序
直接运行检测功能，无需用户输入
"""

import sys
import os
from back_detector import BackDetector

def test_head_detection():
    """测试后脑勺检测功能"""
    print("=" * 50)
    print("           后脑勺检测测试")
    print("=" * 50)
    
    detector = BackDetector()
    
    # 检查摄像头
    print("\n1. 检查摄像头...")
    if not detector.start_camera():
        print("❌ 摄像头启动失败")
        print("请检查：")
        print("- 摄像头是否被其他程序占用")
        print("- 摄像头权限是否已开启")
        print("- 摄像头设备是否正常")
        return False
    
    print("✅ 摄像头启动成功")
    
    # 开始检测
    print("\n2. 开始后脑勺检测...")
    print("请将后脑勺对准摄像头")
    print("按ESC键停止检测")
    
    photo_count = 0
    
    def photo_callback(photo_path):
        nonlocal photo_count
        photo_count += 1
        print(f"✅ 第 {photo_count} 张照片已拍摄: {photo_path}")
    
    try:
        detector.start_detection(photo_callback)
        print(f"\n检测完成，共拍摄了 {photo_count} 张照片")
        return True
    except Exception as e:
        print(f"检测过程中出错: {e}")
        return False
    finally:
        detector.stop_detection()

def main():
    """主函数"""
    print("后脑勺检测拍照系统 - 测试程序")
    
    if test_head_detection():
        print("\n🎉 测试成功！")
        print("系统已准备就绪，可以开始使用后脑勺检测功能")
    else:
        print("\n❌ 测试失败")
        print("请检查系统配置和摄像头权限")

if __name__ == "__main__":
    main()
