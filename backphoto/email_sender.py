import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
from config import EMAIL_CONFIG

class EmailSender:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.sender_email = EMAIL_CONFIG['sender_email']
        self.sender_password = EMAIL_CONFIG['sender_password']
        self.subject = EMAIL_CONFIG['subject']
    
    def send_photo_email(self, recipient_email, photo_path, custom_message=None):
        """
        发送照片邮件
        recipient_email: 收件人邮箱
        photo_path: 照片文件路径
        custom_message: 自定义消息
        """
        try:
            # 检查照片文件是否存在
            if not os.path.exists(photo_path):
                print(f"照片文件不存在: {photo_path}")
                return False
            
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = self.subject
            
            # 邮件正文
            timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
            body = f"""
<html>
<body style="margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;">
    <div style="max-width: 400px; margin: 0 auto; padding: 50px 20px;">
        <h1 style="color: white; font-size: 2.5rem; font-weight: 200; margin-bottom: 40px; text-align: center; letter-spacing: -0.8px; line-height: 1.2; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            The Unseen Portrait
        </h1>
        
        <div style="max-width: 320px; margin: 0 auto; padding: 40px 25px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); border: 1px solid rgba(255, 255, 255, 0.2); text-align: center;">
            <p style="font-size: 18px; font-style: italic; margin-bottom: 30px; color: #4a5568; line-height: 1.6;">
                The first glimpse<br>
                of your unseen self.
            </p>
            
            <p style="font-size: 16px; margin-bottom: 25px; color: #4a5568; line-height: 1.6;">
                We are bound<br>
                to what lies before our eyes,<br>
                as if half the world<br>
                had slipped away unseen.
            </p>
            
            <p style="font-size: 16px; margin-bottom: 0; color: #4a5568; line-height: 1.6;">
                Sometimes,<br>
                the gentlest truths are waiting<br>
                in the places<br>
                we never think to look.
            </p>
            
            <div style="border-top: 1px solid #e2e8f0; padding-top: 25px; margin-top: 30px; text-align: center;">
                <p style="font-size: 14px; color: #666; margin-bottom: 8px; font-weight: 300;">
                    Captured on {timestamp}
                </p>
                <p style="font-size: 14px; color: #666; margin-bottom: 0; font-weight: 300;">
                    © 2025 Yinyin Zhou. All rights reserved.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
"""

            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 添加照片附件
            with open(photo_path, 'rb') as f:
                img_data = f.read()
            
            image = MIMEImage(img_data)
            image.add_header('Content-Disposition', 
                           f'attachment; filename="{os.path.basename(photo_path)}"')
            msg.attach(image)
            
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"照片已成功发送到: {recipient_email}")
            return True
            
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False
    
    def send_photo_email_async(self, recipient_email, photo_path, custom_message=None, callback=None):
        """
        异步发送照片邮件
        callback: 发送完成后的回调函数
        """
        def send_thread():
            success = self.send_photo_email(recipient_email, photo_path, custom_message)
            if callback:
                callback(success, recipient_email, photo_path)
        
        thread = threading.Thread(target=send_thread)
        thread.daemon = True
        thread.start()
    
    def test_connection(self):
        """测试邮件服务器连接"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
            print("邮件服务器连接测试成功")
            return True
        except Exception as e:
            print(f"邮件服务器连接测试失败: {e}")
            return False
    
    def send_test_email(self, recipient_email):
        """发送测试邮件"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "The Unseen Portrait - Test"
            
            body = """
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50; text-align: center; margin-bottom: 30px;">The Unseen Portrait - Test</h2>
                    
                    <p style="font-size: 16px; margin-bottom: 20px;">Hi,</p>
                    
                    <p style="font-size: 16px; margin-bottom: 20px;">
                        This is a test email to verify that the email sending function is working correctly.
                    </p>
                    
                    <p style="font-size: 16px; margin-bottom: 25px;">
                        If you receive this email, it means the email configuration is correct.
                    </p>
                    
                    <div style="border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px;">
                        <p style="font-size: 14px; color: #666; margin-bottom: 0;">
                            Auto Photo System
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"测试邮件已发送到: {recipient_email}")
            return True
            
        except Exception as e:
            print(f"发送测试邮件失败: {e}")
            return False

# 测试函数
if __name__ == "__main__":
    sender = EmailSender()
    
    # 测试连接
    if sender.test_connection():
        print("邮件服务器连接正常")
        
        # 测试发送邮件（需要提供真实的邮箱地址）
        test_email = input("请输入测试邮箱地址: ")
        if test_email:
            sender.send_test_email(test_email)
    else:
        print("请检查邮件配置")