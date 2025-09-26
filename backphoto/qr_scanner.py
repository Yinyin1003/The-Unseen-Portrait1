import cv2
import numpy as np
from pyzbar import pyzbar
import time
from config import QR_CONFIG

class QRScanner:
    def __init__(self):
        self.cap = None
        self.is_scanning = False
        
    def start_camera(self):
        """启动摄像头"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("无法打开摄像头")
            return True
        except Exception as e:
            print(f"启动摄像头失败: {e}")
            return False
    
    def scan_qr_code(self, timeout=None):
        """
        扫描二维码
        返回: (success, data) - (是否成功, 二维码数据)
        """
        if not self.cap:
            if not self.start_camera():
                return False, None
        
        self.is_scanning = True
        start_time = time.time()
        timeout = timeout or QR_CONFIG['timeout']
        
        print("开始扫描二维码...")
        print("请将二维码对准摄像头")
        
        while self.is_scanning:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # 显示摄像头画面
            cv2.imshow('二维码扫描 - 按ESC退出', frame)
            
            # 检测二维码
            qr_codes = pyzbar.decode(frame)
            
            for qr_code in qr_codes:
                data = qr_code.data.decode('utf-8')
                print(f"检测到二维码: {data}")
                
                # 检查是否是期望的二维码
                if data == QR_CONFIG['expected_data']:
                    cv2.destroyAllWindows()
                    self.is_scanning = False
                    return True, data
            
            # 检查超时
            if time.time() - start_time > timeout:
                print("扫描超时")
                cv2.destroyAllWindows()
                self.is_scanning = False
                return False, None
            
            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC键
                print("用户取消扫描")
                cv2.destroyAllWindows()
                self.is_scanning = False
                return False, None
        
        return False, None
    
    def stop_scanning(self):
        """停止扫描"""
        self.is_scanning = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def __del__(self):
        """析构函数"""
        self.stop_scanning()

# 测试函数
if __name__ == "__main__":
    scanner = QRScanner()
    success, data = scanner.scan_qr_code()
    if success:
        print(f"扫描成功: {data}")
    else:
        print("扫描失败")
