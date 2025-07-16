# PoC - FastAPI + Arq 核心链路验证

这个小型的概念验证（PoC）旨在快速验证我们的核心技术架构：通过FastAPI接收HTTP请求，将任务交给`arq`队列，并由一个独立的`arq` worker进程来异步处理这个任务。

这验证了系统中最关键的解耦和异步处理流程。

## 如何运行

**前提:**
- 你已经安装了Python 3.11+
- 你已经安装了此项目的所有依赖 (`pip install -r requirements.txt`)
- 你的本地 `localhost:6379` 上正在运行一个Redis实例。

**步骤:**

1.  **启动服务**:
    在项目根目录下，运行启动脚本。它会同时启动FastAPI Web服务器和Arq后台工作进程。
    ```bash
    bash poc/run_poc.sh
    ```
    你会看到两个服务的启动日志。Worker会在前台运行，方便你观察任务处理的输出。

2.  **发送测试请求**:
    打开一个新的终端，使用 `curl` (或任何HTTP客户端) 向FastAPI服务器发送一个POST请求来创建一个新任务。
    ```bash
    curl -X POST "http://localhost:8000/task?sleep_time=7" -H "accept: application/json"
    ```
    - `sleep_time=7` 参数告诉worker这个任务需要模拟运行7秒钟。
    - 服务器会立刻返回一个JSON响应，告诉你任务已经成功入队。

3.  **观察结果**:
    - **立即响应**: `curl` 命令会几乎立刻收到响应，如 `{"message":"Task enqueued successfully!","job_id":"...","is_queued":true}`。这证明了FastAPI的非阻塞特性。
    - **后台处理**: 切换回运行 `run_poc.sh` 的终端，你会看到Arq Worker打印的日志，类似：
        ```
        16:30:00: [job_id] -> Task received, will run for 7 seconds...
        (等待7秒后)
        16:30:07: [job_id] -> Task finished.
        ```
    这证明了Worker成功地从Redis队列中获取了任务并执行了它。

## 清理

在运行 `run_poc.sh` 的终端中，按下 `Ctrl+C`。脚本会自动停止Worker和后台的FastAPI服务器。
