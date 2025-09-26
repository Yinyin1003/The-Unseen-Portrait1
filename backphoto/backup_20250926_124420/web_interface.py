#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web界面系统
手机扫描二维码 → 手机输入邮箱 → 电脑启动拍照 → 发送邮件 → 回到初始界面
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import time
import os
import sys
from datetime import datetime
import qrcode
from io import BytesIO
import base64

# 导入现有模块
from back_detector import BackDetector
from email_sender import EmailSender

app = Flask(__name__)

# 全局变量
current_email = None
photo_count = 0
detector = None
email_sender = None
is_detecting = False

class WebPhotoSystem:
    def __init__(self):
        self.detector = BackDetector()
        self.email_sender = EmailSender()
        self.current_email = None
        self.photo_count = 0
        self.is_detecting = False
    
    def start_detection(self, email):
        """开始检测和拍照"""
        self.current_email = email
        self.photo_count = 0
        self.is_detecting = True
        
        def photo_callback(photo_path):
            """拍照回调函数"""
            self.photo_count += 1
            print(f"📸 第 {self.photo_count} 张照片已拍摄: {photo_path}")
            
            # 发送邮件
            if self.current_email:
                print(f"📤 正在发送照片到: {self.current_email}")
                self.email_sender.send_photo_email_async(
                    self.current_email, 
                    photo_path,
                    f"这是系统为您自动拍摄的第 {self.photo_count} 张后脑勺照片，请查收。",
                    self.email_sent_callback
                )
        
        try:
            print("🚀 开始后脑勺检测...")
            self.detector.start_detection(photo_callback)
            print(f"✅ 检测完成，共拍摄了 {self.photo_count} 张照片")
        except Exception as e:
            print(f"❌ 检测过程中出错: {e}")
        finally:
            self.is_detecting = False
    
    def email_sent_callback(self, success, email, photo_path):
        """邮件发送回调函数"""
        if success:
            print(f"✅ 照片已成功发送到: {email}")
        else:
            print(f"❌ 照片发送失败: {email}")

# 创建系统实例
photo_system = WebPhotoSystem()

@app.route('/')
def index():
    """主页 - 显示二维码"""
    return render_template('index.html')

@app.route('/api/qr-code')
def generate_qr_code():
    """生成二维码"""
    # 获取本机IP地址
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # 生成二维码内容
    qr_content = f"http://{local_ip}:5000/input"
    
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
    
    return jsonify({
        'qr_code': f"data:image/png;base64,{img_str}",
        'url': qr_content,
        'ip': local_ip
    })

@app.route('/input')
def email_input():
    """邮箱输入页面"""
    return render_template('email_input.html')

@app.route('/api/submit-email', methods=['POST'])
def submit_email():
    """提交邮箱地址"""
    global current_email
    
    data = request.get_json()
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'success': False, 'message': '请输入邮箱地址'})
    
    # 验证邮箱格式
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
    
    current_email = email
    print(f"✅ 收到邮箱地址: {email}")
    
    return jsonify({
        'success': True, 
        'message': '邮箱地址已接收，正在启动拍照程序...',
        'redirect': '/camera'
    })

@app.route('/camera')
def camera_page():
    """拍照页面"""
    return render_template('camera.html', email=current_email)

@app.route('/api/start-camera', methods=['POST'])
def start_camera():
    """启动拍照程序"""
    global current_email, is_detecting
    
    if is_detecting:
        return jsonify({'success': False, 'message': '拍照程序已在运行中'})
    
    if not current_email:
        return jsonify({'success': False, 'message': '请先输入邮箱地址'})
    
    # 在新线程中启动检测
    def run_detection():
        photo_system.start_detection(current_email)
    
    detection_thread = threading.Thread(target=run_detection)
    detection_thread.daemon = True
    detection_thread.start()
    
    is_detecting = True
    
    return jsonify({
        'success': True, 
        'message': '拍照程序已启动，请将后脑勺对准摄像头'
    })

@app.route('/api/stop-camera', methods=['POST'])
def stop_camera():
    """停止拍照程序"""
    global is_detecting
    
    if photo_system.detector and photo_system.detector.cap:
        photo_system.detector.cap.release()
        cv2.destroyAllWindows()
    
    is_detecting = False
    
    return jsonify({
        'success': True, 
        'message': '拍照程序已停止'
    })

@app.route('/api/status')
def get_status():
    """获取系统状态"""
    return jsonify({
        'is_detecting': is_detecting,
        'current_email': current_email,
        'photo_count': photo_system.photo_count
    })

@app.route('/complete')
def complete():
    """完成页面"""
    return render_template('complete.html', 
                         email=current_email, 
                         photo_count=photo_system.photo_count)

def create_templates():
    """创建HTML模板"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # 主页模板
    index_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>后脑勺拍照系统</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 30px; }
        .qr-container { margin: 20px 0; }
        .qr-code { max-width: 300px; margin: 0 auto; }
        .instructions { background: #e8f4fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .status { margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 后脑勺拍照系统</h1>
        <div class="instructions">
            <h3>使用说明：</h3>
            <p>1. 用手机扫描下方二维码</p>
            <p>2. 在手机上输入您的邮箱地址</p>
            <p>3. 电脑将自动启动拍照程序</p>
            <p>4. 照片将自动发送到您的邮箱</p>
        </div>
        <div class="qr-container">
            <div id="qr-code" class="qr-code"></div>
        </div>
        <div class="status">
            <p>系统状态：<span id="status">等待扫描</span></p>
            <p>IP地址：<span id="ip-address"></span></p>
        </div>
    </div>
    
    <script>
        // 加载二维码
        fetch('/api/qr-code')
            .then(response => response.json())
            .then(data => {
                document.getElementById('qr-code').innerHTML = `<img src="${data.qr_code}" alt="二维码">`;
                document.getElementById('ip-address').textContent = data.ip;
            });
        
        // 定期检查状态
        setInterval(() => {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    let status = '等待扫描';
                    if (data.current_email) {
                        status = `已连接 - ${data.current_email}`;
                    }
                    if (data.is_detecting) {
                        status = `拍照中 - 已拍摄 ${data.photo_count} 张`;
                    }
                    document.getElementById('status').textContent = status;
                });
        }, 2000);
    </script>
</body>
</html>'''
    
    # 邮箱输入页面
    email_input_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>输入邮箱地址</title>
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
        <h1>📧 输入邮箱地址</h1>
        <form id="email-form">
            <div class="form-group">
                <label for="email">邮箱地址：</label>
                <input type="email" id="email" name="email" placeholder="例如: user@example.com" required>
            </div>
            <button type="submit">确认</button>
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
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    messageDiv.innerHTML = `<div class="message success">${data.message}</div>`;
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 2000);
                } else {
                    messageDiv.innerHTML = `<div class="message error">${data.message}</div>`;
                }
            });
        });
    </script>
</body>
</html>'''
    
    # 拍照页面
    camera_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>拍照程序</title>
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
        <h1>📸 拍照程序</h1>
        <div class="status">
            <h3>系统状态</h3>
            <p>邮箱地址：<strong id="email-display">{{ email }}</strong></p>
            <p>拍照状态：<span id="camera-status">未启动</span></p>
            <p>已拍摄：<span id="photo-count">0</span> 张照片</p>
        </div>
        
        <div class="controls">
            <button id="start-btn" onclick="startCamera()">启动拍照</button>
            <button id="stop-btn" class="stop" onclick="stopCamera()">停止拍照</button>
        </div>
        
        <div class="info">
            <h4>使用说明：</h4>
            <p>1. 点击"启动拍照"开始检测</p>
            <p>2. 将后脑勺对准电脑摄像头</p>
            <p>3. 系统会自动检测并拍照</p>
            <p>4. 照片将自动发送到您的邮箱</p>
        </div>
        
        <div id="message"></div>
    </div>
    
    <script>
        function startCamera() {
            fetch('/api/start-camera', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('message').innerHTML = 
                        `<div style="background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 10px 0;">${data.message}</div>`;
                    updateStatus();
                });
        }
        
        function stopCamera() {
            fetch('/api/stop-camera', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('message').innerHTML = 
                        `<div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin: 10px 0;">${data.message}</div>`;
                    updateStatus();
                });
        }
        
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('camera-status').textContent = 
                        data.is_detecting ? '拍照中' : '已停止';
                    document.getElementById('photo-count').textContent = data.photo_count || 0;
                });
        }
        
        // 定期更新状态
        setInterval(updateStatus, 2000);
    </script>
</body>
</html>'''
    
    # 完成页面
    complete_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>拍照完成</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #f5f5f5; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #28a745; margin-bottom: 30px; }
        .success { background: #d4edda; color: #155724; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
        button { background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 10px; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ 拍照完成！</h1>
        <div class="success">
            <h3>照片已成功发送</h3>
            <p>邮箱地址：<strong>{{ email }}</strong></p>
            <p>共拍摄：<strong>{{ photo_count }}</strong> 张照片</p>
        </div>
        
        <div class="info">
            <p>请检查您的邮箱，照片应该已经发送到您的邮箱中。</p>
            <p>如果没有收到邮件，请检查垃圾邮件文件夹。</p>
        </div>
        
        <button onclick="location.href='/'">返回首页</button>
        <button onclick="location.href='/input'">重新开始</button>
    </div>
</body>
</html>'''
    
    # 写入模板文件
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    with open(os.path.join(templates_dir, 'email_input.html'), 'w', encoding='utf-8') as f:
        f.write(email_input_html)
    
    with open(os.path.join(templates_dir, 'camera.html'), 'w', encoding='utf-8') as f:
        f.write(camera_html)
    
    with open(os.path.join(templates_dir, 'complete.html'), 'w', encoding='utf-8') as f:
        f.write(complete_html)

if __name__ == '__main__':
    print("🚀 启动Web界面系统...")
    
    # 创建模板文件
    create_templates()
    
    # 检查依赖
    try:
        import cv2
    except ImportError:
        print("❌ 请先安装OpenCV: pip3 install opencv-python")
        sys.exit(1)
    
    print("📱 系统启动完成！")
    print("📱 请在浏览器中访问显示的IP地址")
    print("📱 用手机扫描二维码开始使用")
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=5000, debug=True)
