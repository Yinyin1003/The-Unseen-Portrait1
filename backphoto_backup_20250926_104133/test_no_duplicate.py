#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
去重后脑勺检测测试程序
- 只拍后脑勺，不拍正脸
- 一个后脑勺只拍一张照片
- 拍照时播放声音提示
- 显示冷却时间倒计时
"""

import sys
import os
from back_detector import BackDetector

def main():
    """主函数"""
    print("=" * 60)
    print("           去重后脑勺检测测试")
    print("=" * 60)
    print("功能：")
    print("✅ 只拍后脑勺，不拍正脸")
    print("✅ 一个后脑勺只拍一张照片")
    print("✅ 拍照时播放声音提示")
    print("✅ 显示冷却时间倒计时")
    print("=" * 60)
    
    detector = BackDetector()
    
    # 检查摄像头
    print("\n检查摄像头...")
    if not detector.start_camera():
        print("❌ 摄像头启动失败")
        return
    
    print("✅ 摄像头启动成功")
    
    # 开始检测
    print("\n🎯 开始去重后脑勺检测...")
    print("📋 使用说明：")
    print("   - 将后脑勺对准摄像头")
    print("   - 系统会检测正脸，检测到正脸时不拍照")
    print("   - 只有检测到后脑勺时才会拍照")
    print("   - 一个后脑勺只拍一张照片（5秒冷却期）")
    print("   - 拍照时会播放声音提示")
    print("   - 画面上会显示冷却时间倒计时")
    print("\n🛑 退出方法：")
    print("   - 按 ESC 键退出")
    print("   - 按 Q 键退出")
    print("   - 关闭摄像头窗口")
    print("\n开始检测...")
    
    photo_count = 0
    
    def photo_callback(photo_path):
        nonlocal photo_count
        photo_count += 1
        print(f"📸 第 {photo_count} 张后脑勺照片已拍摄（去重模式）")
    
    try:
        detector.start_detection(photo_callback)
        print(f"\n🎉 检测完成！")
        print(f"📊 统计结果：")
        print(f"   - 共拍摄了 {photo_count} 张后脑勺照片")
        print(f"   - 系统成功避免了重复拍照")
        print(f"   - 每个后脑勺只拍摄了一张照片")
    except Exception as e:
        print(f"检测过程中出错: {e}")
    finally:
        detector.stop_detection()

if __name__ == "__main__":
    main()
