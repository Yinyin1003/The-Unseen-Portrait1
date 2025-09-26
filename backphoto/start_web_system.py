#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
启动Web系统
手机扫描二维码 → 手机输入邮箱 → 电脑启动拍照 → 发送邮件 → 回到初始界面
"""

import os
import sys
import socket
import webbrowser
import time

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 连接到一个远程地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 启动后脑勺拍照Web系统")
    print("=" * 60)
    
    # 获取本机IP
    local_ip = get_local_ip()
    port = 5000
    
    print(f"📱 系统将在以下地址启动：")
    print(f"   电脑访问：http://localhost:{port}")
    print(f"   手机访问：http://{local_ip}:{port}")
    print()
    
    # 检查依赖
    try:
        import flask
        import qrcode
        import cv2
        print("✅ 所有依赖已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip3 install flask qrcode pillow opencv-python")
        return
    
    # 检查邮件配置
    try:
        from config import EMAIL_CONFIG
        if not EMAIL_CONFIG.get('sender_email') or not EMAIL_CONFIG.get('sender_password'):
            print("⚠️  警告：邮件配置不完整，请检查 config.py")
            print("   需要设置 sender_email 和 sender_password")
    except ImportError:
        print("⚠️  警告：未找到 config.py，请先配置邮件设置")
    
    print()
    print("📱 使用说明：")
    print("1. 系统启动后，电脑会显示二维码")
    print("2. 用手机扫描二维码")
    print("3. 在手机上输入邮箱地址")
    print("4. 电脑将自动启动拍照程序")
    print("5. 照片将自动发送到您的邮箱")
    print("6. 完成后可以重新开始")
    print()
    
    # 启动Web系统
    print("🚀 正在启动Web系统...")
    print("📱 请在浏览器中访问显示的地址")
    print("📱 按 Ctrl+C 停止系统")
    print()
    
    # 导入并启动Web系统
    try:
        from web_interface import app
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n⏹️  系统已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查端口5000是否被占用")

if __name__ == "__main__":
    main()
