#!/bin/bash

cd ~/LeetLog

echo "🚀 启动 LeetCode 刷题日志工具..."

# 停止可能残留的进程
pkill -f "python3 app.py" 2>/dev/null
pkill -f "python3 -m http.server" 2>/dev/null
sleep 1

# 启动后端
echo "📡 启动后端服务 (端口 5000)..."
python3 app.py > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid

# 等待后端启动
sleep 2
# 检查后端是否成功
if curl -s http://127.0.0.1:5000/list > /dev/null; then
    echo "✅ 后端启动成功"
else
    echo "❌ 后端启动失败，请查看 backend.log"
    exit 1
fi

# 启动前端
echo "🌐 启动前端服务 (端口 8080)..."
python3 -m http.server 8080 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > frontend.pid

# 等待前端启动
sleep 1
echo "✅ 前端启动成功"
echo ""
echo "🎉 所有服务已启动！"
echo "🌍 访问地址: http://127.0.0.1:8080"
echo "📝 后端日志: backend.log"
echo "📝 前端日志: frontend.log"
echo "🛑 停止服务: ./stop.sh"

# 自动打开浏览器（Linux 桌面环境）
if command -v xdg-open &> /dev/null; then
    xdg-open http://127.0.0.1:8080
elif command -v gnome-open &> /dev/null; then
    gnome-open http://127.0.0.1:8080
elif command -v sensible-browser &> /dev/null; then
    sensible-browser http://127.0.0.1:8080
else
    echo "⚠️ 无法自动打开浏览器，请手动访问 http://127.0.0.1:8080"
fi
