# 配置文件示例
# 请复制此文件为 config.py 并修改相应的配置

# 邮件配置
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Gmail SMTP服务器
    'smtp_port': 587,  # 端口
    'sender_email': 'your_email@gmail.com',  # 发送者邮箱
    'sender_password': 'your_app_password',  # Gmail应用密码（不是登录密码）
    'subject': '自动拍摄照片'
}

# 其他邮件服务器配置示例：
# QQ邮箱：
# 'smtp_server': 'smtp.qq.com'
# 'smtp_port': 587
# 'sender_email': 'your_email@qq.com'
# 'sender_password': 'your_authorization_code'

# 163邮箱：
# 'smtp_server': 'smtp.163.com'
# 'smtp_port': 25
# 'sender_email': 'your_email@163.com'
# 'sender_password': 'your_authorization_code'

# 摄像头配置
CAMERA_CONFIG = {
    'camera_index': 0,  # 摄像头索引，通常0是默认摄像头
    'resolution': (1920, 1080),  # 分辨率
    'fps': 30  # 帧率
}

# 后背检测配置
DETECTION_CONFIG = {
    'confidence_threshold': 0.5,  # 置信度阈值
    'back_detection_area': (0.3, 0.2, 0.4, 0.6),  # 后背检测区域 (x, y, width, height)
    'photo_delay': 2  # 拍照延迟（秒）
}

# 二维码配置
QR_CONFIG = {
    'timeout': 30,  # 扫描超时时间（秒）
    'expected_data': 'backphoto_system'  # 期望的二维码数据
}

# 配置说明：
# 1. 邮件配置：需要设置正确的SMTP服务器和认证信息
# 2. Gmail需要开启两步验证并使用应用密码
# 3. 摄像头索引：如果有多个摄像头，可能需要调整
# 4. 检测区域：根据实际椅子位置调整检测区域
# 5. 二维码数据：可以自定义期望的二维码内容
