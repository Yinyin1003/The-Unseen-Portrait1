import cv2
import numpy as np
import time
import os
import threading
from datetime import datetime
from config import CAMERA_CONFIG, DETECTION_CONFIG

class BackDetector:
    def __init__(self):
        self.cap = None
        self.background_subtractor = None
        self.is_detecting = False
        self.photo_count = 0
        self.face_cascade = None
        self.head_detection_model = None
        self.last_face_detection_time = 0
        self.face_detection_cooldown = DETECTION_CONFIG.get('face_detection_cooldown', 3)
        self.last_photo_time = 0
        self.photo_cooldown = DETECTION_CONFIG.get('photo_cooldown', 5)
        
    def play_sound(self, sound_type="photo"):
        """播放声音提示"""
        # 检查是否启用声音
        if not DETECTION_CONFIG.get('enable_sound', True):
            return
            
        def play_beep():
            try:
                # 使用系统声音
                if sound_type == "photo":
                    # 拍照声音 - 短促的"咔嚓"声
                    os.system('afplay /System/Library/Sounds/Glass.aiff 2>/dev/null || echo "\\a"')
                elif sound_type == "detection":
                    # 检测声音 - 轻柔提示音
                    os.system('afplay /System/Library/Sounds/Ping.aiff 2>/dev/null || echo "\\a"')
            except:
                # 备用方案：使用终端铃声
                print("\\a", end="", flush=True)
        
        # 在单独线程中播放声音，不阻塞主程序
        sound_thread = threading.Thread(target=play_beep)
        sound_thread.daemon = True
        sound_thread.start()
        
    def start_camera(self):
        """启动摄像头"""
        try:
            self.cap = cv2.VideoCapture(CAMERA_CONFIG['camera_index'])
            if not self.cap.isOpened():
                raise Exception("无法打开摄像头")
            
            # 设置摄像头参数
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['resolution'][0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['resolution'][1])
            self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
            
            # 初始化背景减除器
            self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
                detectShadows=True,
                varThreshold=50
            )
            
            # 初始化人脸检测器（用于检测头部区域）
            try:
                self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            except:
                print("警告：无法加载人脸检测器，将使用基础检测方法")
            
            return True
        except Exception as e:
            print(f"启动摄像头失败: {e}")
            return False
    
    def detect_head_back(self, frame):
        """
        检测后脑勺
        使用多种方法结合检测：
        1. 头部区域检测
        2. 背景减除
        3. 边缘检测
        4. 轮廓分析
        """
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 方法1：尝试检测头部区域
        head_region = self.detect_head_region(gray)
        
        # 方法2：背景减除
        fg_mask = self.background_subtractor.apply(gray)
        
        # 形态学操作去噪
        kernel = np.ones((5, 5), np.uint8)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        
        # 方法3：边缘检测
        edges = cv2.Canny(gray, 50, 150)
        
        # 结合多种检测结果
        if head_region is not None:
            # 如果有头部区域，优先使用头部区域
            combined = head_region
        else:
            # 否则使用背景减除和边缘检测
            combined = cv2.bitwise_or(fg_mask, edges)
        
        # 查找轮廓
        contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 分析轮廓
        head_detected = False
        largest_contour = None
        max_area = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area and area > 3000:  # 降低最小面积阈值，适合头部
                max_area = area
                largest_contour = contour
                head_detected = True
        
        return head_detected, largest_contour, combined
    
    def detect_head_region(self, gray):
        """
        检测头部区域
        使用人脸检测器来定位头部区域，然后检测后脑勺
        """
        if self.face_cascade is None:
            return None
        
        # 检测人脸（正面）
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # 如果检测到正面人脸，记录时间并返回None（不拍正脸）
            self.last_face_detection_time = time.time()
            return None
        
        # 检查是否在冷却期内（刚检测到正脸）
        current_time = time.time()
        if current_time - self.last_face_detection_time < self.face_detection_cooldown:
            return None
        
        # 如果没有检测到正面人脸且不在冷却期，可能是后脑勺
        # 使用更宽松的参数检测可能的头部区域
        head_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
        if head_cascade.empty():
            return None
        
        # 检测侧面轮廓
        profiles = head_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(profiles) > 0:
            # 创建头部区域掩码
            mask = np.zeros(gray.shape, dtype=np.uint8)
            for (x, y, w, h) in profiles:
                # 扩展检测区域
                x = max(0, x - w//4)
                y = max(0, y - h//4)
                w = min(gray.shape[1] - x, w + w//2)
                h = min(gray.shape[0] - y, h + h//2)
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
            return mask
        
        return None
    
    def is_in_detection_area(self, contour, frame_shape):
        """检查轮廓是否在检测区域内"""
        if contour is None:
            return False
        
        # 获取轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        
        # 检测区域配置 (x, y, width, height)
        det_x, det_y, det_w, det_h = DETECTION_CONFIG['back_detection_area']
        
        # 转换为像素坐标
        frame_h, frame_w = frame_shape[:2]
        det_x_px = int(det_x * frame_w)
        det_y_px = int(det_y * frame_h)
        det_w_px = int(det_w * frame_w)
        det_h_px = int(det_h * frame_h)
        
        # 检查轮廓中心是否在检测区域内
        center_x = x + w // 2
        center_y = y + h // 2
        
        return (det_x_px <= center_x <= det_x_px + det_w_px and
                det_y_px <= center_y <= det_y_px + det_h_px)
    
    def take_photo(self, frame):
        """拍摄照片"""
        try:
            # 播放拍照声音提示
            self.play_sound("photo")
            
            # 创建照片目录
            photo_dir = "photos"
            if not os.path.exists(photo_dir):
                os.makedirs(photo_dir)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{photo_dir}/photo_{timestamp}_{self.photo_count:03d}.jpg"
            
            # 保存干净的照片（没有框线和文字）
            # 重新从摄像头获取一帧干净的画面
            ret, clean_frame = self.cap.read()
            if ret:
                cv2.imwrite(filename, clean_frame)
            else:
                # 如果无法获取新帧，使用当前帧但去掉所有绘制内容
                cv2.imwrite(filename, frame)
            
            self.photo_count += 1
            
            print(f"📸 照片已保存: {filename}")
            return filename
            
        except Exception as e:
            print(f"拍照失败: {e}")
            return None
    
    def start_detection(self, callback=None):
        """
        开始后背检测
        callback: 检测到后背时的回调函数
        """
        if not self.cap:
            if not self.start_camera():
                return False
        
        self.is_detecting = True
        last_photo_time = 0
        photo_interval = DETECTION_CONFIG['photo_delay']
        
        print("开始后背检测...")
        print("请坐在椅子上，系统将自动检测并拍照")
        print("按ESC键退出检测")
        
        while self.is_detecting:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # 检测后脑勺
            head_detected, contour, mask = self.detect_head_back(frame)
            
            # 检查是否检测到正脸
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4) if self.face_cascade else []
            
            # 绘制检测区域
            frame_h, frame_w = frame.shape[:2]
            det_x, det_y, det_w, det_h = DETECTION_CONFIG['back_detection_area']
            det_x_px = int(det_x * frame_w)
            det_y_px = int(det_y * frame_h)
            det_w_px = int(det_w * frame_w)
            det_h_px = int(det_h * frame_h)
            
            # 根据检测状态改变检测区域颜色
            if len(faces) > 0:
                # 检测到正脸，显示红色警告
                cv2.rectangle(frame, (det_x_px, det_y_px), 
                             (det_x_px + det_w_px, det_y_px + det_h_px), 
                             (0, 0, 255), 3)
                cv2.putText(frame, "FACE DETECTED - NO PHOTO", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            #
            
            # 如果检测到后脑勺且在检测区域内，且没有检测到正脸
            if head_detected and self.is_in_detection_area(contour, frame.shape) and len(faces) == 0:
                current_time = time.time()
                
                # 绘制检测框
                if contour is not None:
                    x, y, w, h = cv2.boundingRect(contour)
                
                    cv2.putText(frame, "Head Back Detected!", (x, y - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # 检查拍照间隔和去重机制
                if (current_time - last_photo_time > photo_interval and 
                    current_time - self.last_photo_time > self.photo_cooldown):
                    print("检测到后脑勺，准备拍照...")
                    time.sleep(0.5)  # 短暂延迟确保稳定
                    
                    # 拍照
                    photo_path = self.take_photo(frame)
                    if photo_path and callback:
                        callback(photo_path)
                    
                    last_photo_time = current_time
                    self.last_photo_time = current_time  # 记录最后拍照时间
                else:
                    # 显示等待提示
                    remaining_time = max(0, self.photo_cooldown - (current_time - self.last_photo_time))
                    cv2.putText(frame, f"Photo cooldown: {remaining_time:.1f}s", (10, 90), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            else:
                cv2.putText(frame, "Waiting for head back...", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # 添加退出提示
            cv2.putText(frame, "Press ESC or Q to exit", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # 显示画面
            cv2.imshow('后脑勺检测 - 按ESC键退出', frame)
            
            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC键
                print("\n🛑 用户按ESC键停止检测")
                self.is_detecting = False
            elif key == ord('q') or key == ord('Q'):  # Q键
                print("\n🛑 用户按Q键停止检测")
                self.is_detecting = False
        
        cv2.destroyAllWindows()
        return True
    
    def stop_detection(self):
        """停止检测"""
        self.is_detecting = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def __del__(self):
        """析构函数"""
        self.stop_detection()

# 测试函数
if __name__ == "__main__":
    detector = BackDetector()
    
    def photo_callback(photo_path):
        print(f"照片已拍摄: {photo_path}")
    
    detector.start_detection(photo_callback)
