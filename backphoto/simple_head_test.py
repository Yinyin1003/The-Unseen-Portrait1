#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的后脑勺检测测试程序
- 只拍后脑勺，不拍正脸
- 拍照时播放声音提示
- 明确的退出说明
"""

import sys
import os
from back_detector import BackDetector

def main():
    """主函数"""
    print("=" * 60)
    print("           简单后脑勺检测测试")
    print("=" * 60)
    print("功能：只拍后脑勺，不拍正脸，拍照时有声音提示")
    print("=" * 60)
    
    detector = BackDetector()
    
    # 检查摄像头
    print("\n检查摄像头...")
    if not detector.start_camera():
        print("❌ 摄像头启动失败")
        return
    
    print("✅ 摄像头启动成功")
    
    # 开始检测
    print("\n🎯 开始后脑勺检测...")
    print("📋 使用说明：")
    print("   - 将后脑勺对准摄像头")
    print("   - 系统会检测正脸，检测到正脸时不拍照")
    print("   - 只有检测到后脑勺时才会拍照")
    print("   - 拍照时会播放声音提示")
    print("\n🛑 退出方法：")
    print("   - 按 ESC 键退出")
    print("   - 按 Q 键退出")
    print("   - 关闭摄像头窗口")
    print("\n开始检测...")
    
    photo_count = 0
    
    def photo_callback(photo_path):
        nonlocal photo_count
        photo_count += 1
        print(f"📸 第 {photo_count} 张后脑勺照片已拍摄")
    
    try:
        detector.start_detection(photo_callback)
        print(f"\n🎉 检测完成！共拍摄了 {photo_count} 张后脑勺照片")
    except Exception as e:
        print(f"检测过程中出错: {e}")
    finally:
        detector.stop_detection()

if __name__ == "__main__":
    main()
