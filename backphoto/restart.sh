#!/bin/bash

echo "🔄 重启 The Unseen Portrait 系统..."

# 停止所有Python进程
echo "🛑 停止旧进程..."
pkill -f "python" 2>/dev/null

# 释放8080端口
echo "🔌 释放8080端口..."
lsof -ti:8080 | xargs kill -9 2>/dev/null

# 等待3秒
echo "⏱️ 等待3秒..."
sleep 3

# 启动系统
echo "🚀 启动系统..."
cd /Users/zhouyinyin/Downloads/The\ Unseen\ Portrait/The-Unseen-Portrait/backphoto
python3 simple_web_system.py


