#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动拍照系统启动脚本
简化版本，直接启动自动拍照流程
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import AutoPhotoSystem

def quick_start():
    """快速启动自动拍照流程"""
    print("=" * 50)
    print("    自动拍照系统 - 快速启动")
    print("=" * 50)
    print("系统将依次执行：")
    print("1. 扫描二维码")
    print("2. 输入邮箱")
    print("3. 自动检测后背并拍照")
    print("4. 发送照片到邮箱")
    print("=" * 50)
    
    input("按回车键开始...")
    
    try:
        system = AutoPhotoSystem()
        system.start_auto_photo_workflow()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        print("程序结束")

if __name__ == "__main__":
    quick_start()
