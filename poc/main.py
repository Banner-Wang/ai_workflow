import os
from fastapi import FastAPI
from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

app = FastAPI(title="PoC - FastAPI + Arq")


# Redis配置，必须与worker.py中的配置一致
# 从环境变量中读取密码，而不是硬编码
REDIS_SETTINGS = RedisSettings(
    host='localhost', 
    port=6379, 
    password=os.getenv("REDIS_PASSWORD", "123456")
)
# Arq的Redis连接池
ARQ_POOL: ArqRedis | None = None

@app.on_event("startup")
async def startup():
    """在应用启动时创建arq连接池"""
    global ARQ_POOL
    ARQ_POOL = await create_pool(REDIS_SETTINGS)

@app.on_event("shutdown")
async def shutdown():
    """在应用关闭时关闭arq连接池"""
    if ARQ_POOL:
        await ARQ_POOL.close()

@app.post("/task", summary="Enqueue a new task")
async def create_task(sleep_time: int = 5):
    """
    接收请求，并将一个名为'heavy_task'的作业推送到Redis队列中。
    这个作业将由一个独立的arq worker进程来执行。
    """
    if not ARQ_POOL:
        return {"error": "Redis pool not initialized"}, 500

    # 将任务推入队列
    # 'heavy_task' 对应 worker.py 中 WorkerSettings.functions 列表里的函数名
    job = await ARQ_POOL.enqueue_job("heavy_task", sleep_time=sleep_time)

    if job:
        return {
            "message": "Task enqueued successfully!",
            "job_id": job.job_id,
            "is_queued": await job.status() == "queued"
        }
    else:
        return {"error": "Failed to enqueue task"}, 500
