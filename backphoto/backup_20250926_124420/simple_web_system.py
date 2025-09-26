#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化Web系统
手机扫描二维码 → 手机输入邮箱 → 电脑启动拍照 → 发送邮件 → 回到初始界面
"""

import os
import sys
import socket
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import qrcode
from io import BytesIO
import base64

# 导入现有模块
from back_detector import BackDetector
from email_sender import EmailSender

class SimpleWebHandler(BaseHTTPRequestHandler):
    """简单的HTTP请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.serve_index()
        elif self.path == '/qr-code':
            self.serve_qr_code()
        elif self.path == '/input':
            self.serve_email_input()
        elif self.path == '/camera':
            self.serve_camera()
        elif self.path == '/api/status':
            self.serve_status()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/submit-email':
            self.handle_submit_email()
        elif self.path == '/api/start-camera':
            self.handle_start_camera()
        elif self.path == '/api/stop-camera':
            self.handle_stop_camera()
        else:
            self.send_error(404)
    
    def serve_index(self):
        """主页 - 显示二维码"""
        local_ip = self.get_local_ip()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Unseen Portrait</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; margin-bottom: 30px; }}
        .qr-container {{ margin: 20px 0; }}
        .qr-code {{ max-width: 300px; margin: 0 auto; }}
        .instructions {{ background: #e8f4fd; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .status {{ margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 The Unseen Portrait</h1>
        <div class="instructions">
            <h3>Instructions:</h3>
            <p>1. Scan the QR code below with your phone</p>
            <p>2. Enter your email address on your phone</p>
            <p>3. The computer will automatically start the photo program</p>
            <p>4. Photos will be automatically sent to your email</p>
        </div>
        <div class="qr-container">
            <div id="qr-code" class="qr-code"></div>
        </div>
        <div class="status">
            <p>System Status: <span id="status">Waiting for scan</span></p>
            <p>IP Address: {local_ip}</p>
        </div>
    </div>
    
    <script>
        // Load QR code
        fetch('/qr-code')
            .then(response => response.text())
            .then(data => {{
                document.getElementById('qr-code').innerHTML = data;
            }});
        
        // Check status periodically
        setInterval(() => {{
            fetch('/api/status')
                .then(response => response.text())
                .then(data => {{
                    try {{
                        const status = JSON.parse(data);
                        let statusText = 'Waiting for scan';
                        if (status.current_email) {{
                            statusText = `Connected - ${{status.current_email}}`;
                        }}
                        if (status.is_detecting) {{
                            statusText = `Taking photos - ${{status.photo_count}} photos taken`;
                        }}
                        document.getElementById('status').textContent = statusText;
                    }} catch (e) {{
                        // Ignore parsing errors
                    }}
                }});
        }}, 2000);
    </script>
</body>
</html>'''
        
        self.wfile.write(html.encode('utf-8'))
    
    def serve_qr_code(self):
        """生成二维码"""
        local_ip = self.get_local_ip()
        qr_content = f"http://{local_ip}:8080/input"
        
        # 生成二维码
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        # 创建二维码图片
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 转换为base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f'<img src="data:image/png;base64,{img_str}" alt="二维码" style="max-width: 300px;">'
        self.wfile.write(html.encode('utf-8'))
    
    def serve_email_input(self):
        """邮箱输入页面"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enter Email Address</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #f5f5f5; }
        .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 30px; }
        .form-group { margin: 20px 0; text-align: left; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="email"] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%; }
        button:hover { background: #0056b3; }
        .message { margin: 20px 0; padding: 10px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📧 Enter Email Address</h1>
        <form id="email-form">
            <div class="form-group">
                <label for="email">Email Address:</label>
                <input type="email" id="email" name="email" placeholder="e.g. user@example.com" required>
            </div>
            <button type="submit">Submit</button>
        </form>
        <div id="message"></div>
    </div>
    
    <script>
        document.getElementById('email-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const messageDiv = document.getElementById('message');
            
            fetch('/api/submit-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'email=' + encodeURIComponent(email)
            })
            .then(response => response.text())
            .then(data => {
                if (data.includes('success')) {
                    messageDiv.innerHTML = '<div class="message success">Email received, starting photo program...</div>';
                    setTimeout(() => {
                        window.location.href = '/camera';
                    }, 2000);
                } else {
                    messageDiv.innerHTML = '<div class="message error">' + data + '</div>';
                }
            });
        });
    </script>
</body>
</html>'''
        
        self.wfile.write(html.encode('utf-8'))
    
    def serve_camera(self):
        """拍照页面"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Unseen Portrait - Camera</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 30px; }
        .status { background: #e8f4fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .controls { margin: 20px 0; }
        button { background: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 0 10px; }
        button:hover { background: #218838; }
        button.stop { background: #dc3545; }
        button.stop:hover { background: #c82333; }
        .info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 The Unseen Portrait</h1>
        <div class="status">
            <h3>System Status</h3>
            <p>Camera Status: <span id="camera-status">Not Started</span></p>
            <p>Photos Taken: <span id="photo-count">0</span> photos</p>
        </div>
        
        <div class="controls">
            <button id="start-btn" onclick="startCamera()">Start Camera</button>
            <button id="stop-btn" class="stop" onclick="stopCamera()">Stop Camera</button>
        </div>
        
        <div class="info">
            <h4>Instructions:</h4>
            <p>1. Click "Start Camera" to begin detection</p>
            <p>2. Position the back of your head towards the camera</p>
            <p>3. The system will automatically detect and take photos</p>
            <p>4. Photos will be automatically sent to your email</p>
        </div>
        
        <div id="message"></div>
    </div>
    
    <script>
        function startCamera() {
            fetch('/api/start-camera', { method: 'POST' })
                .then(response => response.text())
                .then(data => {
                    document.getElementById('message').innerHTML = 
                        '<div style="background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 10px 0;">' + data + '</div>';
                    updateStatus();
                });
        }
        
        function stopCamera() {
            fetch('/api/stop-camera', { method: 'POST' })
                .then(response => response.text())
                .then(data => {
                    document.getElementById('message').innerHTML = 
                        '<div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin: 10px 0;">' + data + '</div>';
                    updateStatus();
                });
        }
        
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.text())
                .then(data => {
                    try {
                        const status = JSON.parse(data);
                        document.getElementById('camera-status').textContent = 
                            status.is_detecting ? 'Taking Photos' : 'Stopped';
                        document.getElementById('photo-count').textContent = status.photo_count || 0;
                    } catch (e) {
                        // Ignore parsing errors
                    }
                });
        }
        
        // Update status periodically
        setInterval(updateStatus, 2000);
    </script>
</body>
</html>'''
        
        self.wfile.write(html.encode('utf-8'))
    
    def serve_status(self):
        """获取系统状态"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        status = {
            'is_detecting': getattr(self.server, 'is_detecting', False),
            'current_email': getattr(self.server, 'current_email', None),
            'photo_count': getattr(self.server, 'photo_count', 0)
        }
        
        self.wfile.write(json.dumps(status).encode('utf-8'))
    
    def handle_submit_email(self):
        """处理邮箱提交"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        email = data.get('email', [''])[0].strip()
        
        if not email:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Please enter an email address'.encode('utf-8'))
            return
        
        # 验证邮箱格式
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Please enter a valid email address'.encode('utf-8'))
            return
        
        # 保存邮箱
        self.server.current_email = email
        self.server.photo_count = 0
        
        print(f"✅ 收到邮箱地址: {email}")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('success'.encode('utf-8'))
    
    def handle_start_camera(self):
        """启动拍照程序"""
        if self.server.is_detecting:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Camera program is already running'.encode('utf-8'))
            return
        
        if not self.server.current_email:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Please enter an email address first'.encode('utf-8'))
            return
        
        # 在新线程中启动检测
        def run_detection():
            try:
                detector = BackDetector()
                email_sender = EmailSender()
                
                def photo_callback(photo_path):
                    self.server.photo_count += 1
                    print(f"📸 第 {self.server.photo_count} 张照片已拍摄: {photo_path}")
                    
                    # 发送邮件
                    if self.server.current_email:
                        print(f"📤 正在发送照片到: {self.server.current_email}")
                        email_sender.send_photo_email_async(
                            self.server.current_email, 
                            photo_path,
                            f"This is the {self.server.photo_count}th photo automatically taken by The Unseen Portrait system. Please check your email.",
                            lambda success, email, path: print(f"✅ Email sent {'successfully' if success else 'failed'}: {email}")
                        )
                
                print("🚀 Starting head detection...")
                detector.start_detection(photo_callback)
                print(f"✅ Detection completed, {self.server.photo_count} photos taken")
            except Exception as e:
                print(f"❌ Error during detection: {e}")
            finally:
                self.server.is_detecting = False
        
        detection_thread = threading.Thread(target=run_detection)
        detection_thread.daemon = True
        detection_thread.start()
        
        self.server.is_detecting = True
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Camera program started, please position the back of your head towards the camera'.encode('utf-8'))
    
    def handle_stop_camera(self):
        """停止拍照程序"""
        self.server.is_detecting = False
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Camera program stopped'.encode('utf-8'))
    
    def get_local_ip(self):
        """获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def log_message(self, format, *args):
        """重写日志方法，减少输出"""
        pass

class SimpleWebServer:
    """简单Web服务器"""
    
    def __init__(self, port=8080):
        self.port = port
        self.server = None
    
    def start(self):
        """启动服务器"""
        try:
            self.server = HTTPServer(('0.0.0.0', self.port), SimpleWebHandler)
            self.server.current_email = None
            self.server.photo_count = 0
            self.server.is_detecting = False
            
            local_ip = self.get_local_ip()
            print("=" * 60)
            print("🚀 The Unseen Portrait Web System Started")
            print("=" * 60)
            print(f"📱 Computer Access: http://localhost:{self.port}")
            print(f"📱 Mobile Access: http://{local_ip}:{self.port}")
            print()
            print("📱 Instructions:")
            print("1. Scan the QR code displayed on the computer with your phone")
            print("2. Enter your email address on your phone")
            print("3. The computer will automatically start the photo program")
            print("4. Photos will be automatically sent to your email")
            print("5. Press Ctrl+C to stop the system")
            print()
            
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️  System stopped")
        except Exception as e:
            print(f"❌ Startup failed: {e}")
    
    def get_local_ip(self):
        """获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

def main():
    """主函数"""
    # 检查依赖
    try:
        import cv2
        from back_detector import BackDetector
        from email_sender import EmailSender
        print("✅ All dependencies checked")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install: pip3 install opencv-python")
        return
    
    # 检查邮件配置
    try:
        from config import EMAIL_CONFIG
        if not EMAIL_CONFIG.get('sender_email') or not EMAIL_CONFIG.get('sender_password'):
            print("⚠️  Warning: Email configuration incomplete, please check config.py")
    except ImportError:
        print("⚠️  Warning: config.py not found, please configure email settings first")
    
    # 启动Web服务器
    web_server = SimpleWebServer(port=8080)
    web_server.start()

if __name__ == "__main__":
    main()
