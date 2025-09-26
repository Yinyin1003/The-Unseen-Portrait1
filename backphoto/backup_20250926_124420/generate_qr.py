#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
二维码生成工具
用于生成系统所需的二维码
"""

import qrcode
import os
from config import QR_CONFIG

def generate_qr_code(data=None, filename="qr_code.png"):
    """
    生成二维码
    data: 二维码数据，默认使用配置文件中的数据
    filename: 保存的文件名
    """
    if data is None:
        data = QR_CONFIG['expected_data']
    
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,  # 控制二维码的大小
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 错误纠正级别
        box_size=10,  # 每个小方块的像素数
        border=4,  # 边框的厚度
    )
    
    # 添加数据
    qr.add_data(data)
    qr.make(fit=True)
    
    # 创建二维码图像
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 保存图像
    img.save(filename)
    print(f"二维码已生成: {filename}")
    print(f"二维码数据: {data}")
    
    return filename

def generate_multiple_qr_codes():
    """生成多个测试用的二维码"""
    test_data = [
        QR_CONFIG['expected_data'],  # 正确的数据
        "test_qr_1",
        "test_qr_2",
        "invalid_qr"  # 无效数据
    ]
    
    for i, data in enumerate(test_data):
        filename = f"qr_code_{i+1}.png"
        generate_qr_code(data, filename)
    
    print(f"\n已生成 {len(test_data)} 个测试二维码")

if __name__ == "__main__":
    print("二维码生成工具")
    print("=" * 30)
    
    while True:
        print("\n请选择操作：")
        print("1. 生成系统二维码")
        print("2. 生成自定义二维码")
        print("3. 生成多个测试二维码")
        print("0. 退出")
        
        choice = input("请输入选择: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            generate_qr_code()
        elif choice == "2":
            data = input("请输入二维码数据: ").strip()
            if data:
                filename = input("请输入文件名 (默认: custom_qr.png): ").strip()
                if not filename:
                    filename = "custom_qr.png"
                generate_qr_code(data, filename)
        elif choice == "3":
            generate_multiple_qr_codes()
        else:
            print("无效选择")
    
    print("程序结束")
