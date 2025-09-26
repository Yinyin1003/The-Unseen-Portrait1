# 自动拍照系统

这是一个自动拍照系统，客户坐在固定位置的椅子上，扫描二维码，输入邮箱，系统会自动识别后背并拍摄照片发送到指定邮箱。

## 功能特点

- ✅ 二维码扫描识别
- ✅ 邮箱输入界面
- ✅ 后背识别和自动拍照
- ✅ 自动邮件发送
- ✅ 完整的测试功能
- ✅ 配置管理

## 系统要求

- Python 3.7+
- 摄像头设备
- 网络连接（用于发送邮件）

## 安装步骤

1. **安装Python依赖**
```bash
pip install -r requirements.txt
```

2. **配置系统**
```bash
# 复制配置文件
cp config_example.py config.py

# 编辑配置文件，设置邮件服务器信息
nano config.py
```

3. **生成测试二维码**
```bash
python generate_qr.py
```

## 使用方法

### 快速启动
```bash
python start.py
```

### 完整功能
```bash
python main.py
```

### 工作流程
1. 客户扫描二维码
2. 输入邮箱地址
3. 坐在椅子上
4. 系统自动识别后背并拍照
5. 照片自动发送到指定邮箱

## 配置说明

### 邮件配置
在 `config.py` 中配置邮件服务器：

**Gmail配置示例：**
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',  # 应用密码，不是登录密码
    'subject': '自动拍摄照片'
}
```

**获取Gmail应用密码：**
1. 开启两步验证
2. 生成应用密码
3. 使用应用密码而不是登录密码

### 摄像头配置
```python
CAMERA_CONFIG = {
    'camera_index': 0,  # 摄像头索引
    'resolution': (1920, 1080),  # 分辨率
    'fps': 30  # 帧率
}
```

### 检测配置
```python
DETECTION_CONFIG = {
    'confidence_threshold': 0.5,  # 置信度阈值
    'back_detection_area': (0.3, 0.2, 0.4, 0.6),  # 检测区域
    'photo_delay': 2  # 拍照延迟
}
```

## 测试功能

系统提供完整的测试功能：

1. **测试二维码扫描** - 验证二维码识别功能
2. **测试邮箱输入** - 验证邮箱输入界面
3. **测试后背检测** - 验证后背识别功能
4. **测试邮件发送** - 验证邮件发送功能
5. **配置检查** - 检查系统配置

## 文件结构

```
backphoto/
├── main.py              # 主程序
├── start.py             # 快速启动脚本
├── config.py            # 配置文件
├── config_example.py    # 配置示例
├── qr_scanner.py        # 二维码扫描模块
├── email_input.py       # 邮箱输入模块
├── back_detector.py     # 后背检测模块
├── email_sender.py      # 邮件发送模块
├── generate_qr.py       # 二维码生成工具
├── requirements.txt     # 依赖列表
├── README.md           # 说明文档
└── photos/             # 照片保存目录（自动创建）
```

## 故障排除

### 常见问题

1. **摄像头无法打开**
   - 检查摄像头是否被其他程序占用
   - 尝试更改 `camera_index` 值
   - 检查摄像头权限

2. **邮件发送失败**
   - 检查网络连接
   - 验证邮件服务器配置
   - 确认应用密码正确

3. **后背检测不准确**
   - 调整检测区域配置
   - 确保光线充足
   - 调整置信度阈值

4. **二维码扫描失败**
   - 确保二维码清晰可见
   - 检查二维码数据是否正确
   - 调整摄像头位置

## 注意事项

- 确保摄像头权限已开启
- 需要配置有效的邮件服务器
- 建议在固定位置使用以获得最佳效果
- 定期清理 `photos` 目录中的照片文件
- 建议在稳定的网络环境下使用

## 技术支持

如遇到问题，请检查：
1. Python版本是否符合要求
2. 所有依赖是否正确安装
3. 配置文件是否正确设置
4. 硬件设备是否正常工作

---

## English Version / 英文版本

### Quick Start (English)

For English users, please refer to the following files:

- **README_EN.md** - Complete English documentation
- **Email_Configuration_EN.md** - Email setup guide in English
- **simple_head_test_en.py** - English head detection test
- **english_workflow.py** - Complete English workflow
- **test_email_en.py** - English email configuration test

### English Usage

```bash
# Test head detection (English)
python3 simple_head_test_en.py

# Test email configuration (English)
python3 test_email_en.py

# Complete workflow (English)
python3 english_workflow.py
```

### English Email Template

The system now sends emails with a beautiful English template:

**Subject**: The Unseen Portrait

**Content**:
```
Hi,

The first glimpse
of your unseen self.

Sometimes the gentlest truths
are found
in the places we never look.

Here's to a day that feels new,
as if the world
has just begun again. 🌿

Captured on [timestamp]

Yinyin Zhou
```
