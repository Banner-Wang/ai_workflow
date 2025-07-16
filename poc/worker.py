import asyncio
import os
from arq import create_pool
from arq.connections import RedisSettings

# 任务函数，模拟耗时的I/O操作
async def heavy_task(ctx, sleep_time: int = 5):
    """
    一个模拟的耗时任务
    :param ctx: arq上下文，包含redis连接等信息
    :param sleep_time: 模拟执行所需的时间
    """
    job_id = ctx['job_id']
    print(f"[{job_id}] -> Task received, will run for {sleep_time} seconds...")
    await asyncio.sleep(sleep_time)
    print(f"[{job_id}] -> Task finished.")
    return f"Slept for {sleep_time} seconds."

# Arq Worker 的配置
# 这定义了worker需要连接的Redis以及它能够处理的任务列表
class WorkerSettings:
    functions = [heavy_task]  # 声明此worker可以执行的任务
    redis_settings = RedisSettings(
        host='localhost', 
        port=6379, 
        password=os.getenv("REDIS_PASSWORD", "123456")
    )
    job_timeout = 10  # 任务超时时间为10秒
    max_tries = 3     # 最多重试3次
