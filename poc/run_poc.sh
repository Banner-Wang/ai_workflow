#!/bin/bash
# 这是一个简单的脚本，用于启动PoC所需的服务

# 启动 FastAPI/Uvicorn 服务器 (后台运行)
echo "Starting FastAPI server in the background..."
uvicorn poc.main:app --host 0.0.0.0 --port 8182 &
UVICORN_PID=$!
echo "FastAPI server started with PID: $UVICORN_PID"

echo ""
echo "-------------------------------------------------"
echo ""

# 启动 Arq Worker (前台运行，以便观察日志)
# 它会加载 poc.worker.py 中的 WorkerSettings
echo "Starting Arq worker in the foreground..."
echo "Press Ctrl+C to stop both the worker and the server."
arq poc.worker.WorkerSettings --watch poc

# 当用户按下 Ctrl+C 停止 worker 时，也一并停止后台的 uvicorn 进程
echo "Stopping FastAPI server..."
kill $UVICORN_PID
echo "Cleanup complete."
