#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

class EmailInputWindow(QMainWindow):
    email_submitted = pyqtSignal(str)
    cancelled = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.email = None
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("邮箱输入 - PyQt版本")
        self.setGeometry(300, 300, 500, 300)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            QLabel#info {
                font-size: 12px;
                color: #7f8c8d;
                padding: 5px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QPushButton#submit {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton#submit:hover {
                background-color: #229954;
            }
            QPushButton#cancel {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton#cancel:hover {
                background-color: #c0392b;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 标题
        title = QLabel("📧 邮箱输入")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # 说明
        info = QLabel("请输入您的邮箱地址：")
        info.setObjectName("info")
        info.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info)
        
        # 输入框
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("例如: user@example.com")
        self.email_input.returnPressed.connect(self.submit_email)
        main_layout.addWidget(self.email_input)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        # 确认按钮
        submit_btn = QPushButton("确认")
        submit_btn.setObjectName("submit")
        submit_btn.clicked.connect(self.submit_email)
        button_layout.addWidget(submit_btn)
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setObjectName("cancel")
        cancel_btn.clicked.connect(self.cancel_input)
        button_layout.addWidget(cancel_btn)
        
        # 设置焦点
        self.email_input.setFocus()
        
        # 居中显示
        self.center_window()
    
    def center_window(self):
        """窗口居中显示"""
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def submit_email(self):
        """提交邮箱"""
        email = self.email_input.text().strip()
        
        if not email:
            QMessageBox.warning(self, "错误", "请输入邮箱地址")
            return
        
        if not validate_email(email):
            QMessageBox.warning(self, "错误", "请输入有效的邮箱地址")
            return
        
        self.email = email
        print(f"✅ 用户输入邮箱: {email}")
        self.email_submitted.emit(email)
        self.close()
    
    def cancel_input(self):
        """取消输入"""
        print("❌ 用户取消输入")
        self.cancelled.emit()
        self.close()

def pyqt_email_input():
    """使用PyQt创建邮箱输入界面"""
    print("🚀 启动PyQt邮箱输入窗口...")
    
    app = QApplication(sys.argv)
    window = EmailInputWindow()
    
    result = {"email": None}
    
    def on_email_submitted(email):
        result["email"] = email
    
    def on_cancelled():
        result["email"] = None
    
    window.email_submitted.connect(on_email_submitted)
    window.cancelled.connect(on_cancelled)
    
    window.show()
    print("📱 PyQt窗口应该已经显示...")
    
    app.exec_()
    return result["email"]

if __name__ == "__main__":
    print("=" * 50)
    print("开始运行PyQt邮箱输入程序")
    print("=" * 50)
    
    email = pyqt_email_input()
    
    print("=" * 50)
    if email:
        print(f"✅ 成功获取邮箱: {email}")
    else:
        print("❌ 未获取到邮箱")
    print("=" * 50)
