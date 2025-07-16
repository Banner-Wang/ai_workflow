# **开发任务与里程碑计划**

*   **文档版本**: 1.3
*   **更新日期**: 2025年7月16日

## **概述**

本文档将项目开发过程分解为五个主要里程碑，以一个核心功能的概念验证(PoC)作为开端，确保关键技术路径的通畅，随后进行稳步开发。

---

## **里程碑 0: 核心逻辑概念验证 (PoC)**

*   **目标**: 在全面开发前，通过一个最小化、可运行的Demo，验证 "FastAPI -> Arq -> Worker" 这一核心技术链路是通畅的，以降低后续开发风险。
*   **预计周期**: <1天

| 任务 ID | 任务名称 | 详细描述 | 状态 |
| --- | --- | --- | --- |
| **0.1** | **创建PoC目录** | 创建 `poc/` 目录用于存放所有验证相关文件。 | `completed` |
| **0.2** | **编写PoC代码** | 1. 创建 `poc/main.py`，包含一个FastAPI端点用于任务入队。<br>2. 创建 `poc/worker.py`，定义Arq Worker和模拟的任务函数。 | `completed` |
| **0.3** | **编写PoC运行脚本** | 创建 `poc/run_poc.sh` 脚本，用于一键启动FastAPI服务和Arq Worker。<br>创建 `poc/README.md` 解释如何运行和测试。 | `completed` |
| **0.4** | **执行与验证** | 遵循 `poc/README.md` 中的步骤，启动服务，发送测试请求，并观察Worker日志，确认端到端流程符合预期。 | `completed` |

---

## **里程碑 1: 项目初始化与核心基础构建**

*   **目标**: 搭建项目骨架，完成数据库建模与配置，为后续功能开发奠定坚实基础。
*   **预计周期**: 2-3天

| 任务 ID | 任务名称 | 详细描述 | 状态 |
| --- | --- | --- | --- |
| **1.1** | **初始化项目结构** | 根据 `docs/architecture.md` 中定义的目录结构图，创建所有必要的文件夹和空的 `__init__.py` 文件。 | `completed` |
| **1.2** | **配置依赖管理** | 创建 `requirements.txt` 文件，并列出所有核心依赖及其推荐版本（fastapi, uvicorn, sqlalchemy, asyncmy, alembic, arq, pydantic-settings）。 | `completed` |
| **1.3** | **配置核心应用** | 1. 在 `src/main.py` 中创建 FastAPI 应用实例。<br>2. 在 `src/core/config.py` 中使用 `pydantic-settings` 定义配置模型。<br>3. 在 `src/core/database.py` 中配置 SQLAlchemy 的异步数据库引擎和会话管理。 | `to_do` |
| **1.4** | **数据库建模与迁移** | 1. 在 `src/models/` 目录下为 `Task` 和 `Tag` 实体（包括`task_tags`关联表）创建 SQLAlchemy 模型。<br>2. 初始化 Alembic，生成初版数据库迁移脚本。 | `to_do` |
| **1.5** | **定义Pydantic Schemas** | 在 `src/schemas/` 目录下，为API的数据交互（如 `TaskCreate`, `TaskRead`）创建 Pydantic 模型。 | `to_do` |

---

## **里程碑 2: API 端点实现**

*   **目标**: 根据产品需求文档（PRD）完成所有核心 RESTful API 端点的开发与调试。
*   **预计周期**: 3-5天

| 任务 ID | 任务名称 | 详细描述 | 状态 |
| --- | --- | --- | --- |
| **2.1** | **实现CRUD业务逻辑** | 在 `src/crud/` 目录下，编写针对 `Task` 和 `Tag` 实体的增删改查业务逻辑函数。 | `to_do` |
| **2.2** | **实现 `POST /tasks`** | 创建新任务的端点。此接口将调用CRUD服务创建任务，并使用 `arq` 将任务处理作业推入队列。 | `to_do` |
| **2.3** | **实现 `GET /tasks`** | 实现查询任务列表的端点，并支持按 `status`, `priority`, `tag` 进行复合查询。 | `to_do` |
| **2.4** | **实现 `GET /tasks/{id}`**| 实现获取单个任务详情的端点。 | `to_do` |
| **2.5** | **实现 `PATCH /tasks/{id}`**| 实现更新任务元数据（如标题、优先级）的端点。 | `to_do` |
| **2.6** | **实现 `DELETE /tasks/{id}`**| 实现删除任务的端点。 | `to_do` |
| **2.7** | **统一错误处理** | 实现健壮的API错误处理机制，例如，统一处理404 (Not Found) 等HTTP异常。 | `to_do` |

---

## **里程碑 3: 后台 Worker 与任务处理**

*   **目标**: 实现 `arq` Worker，使其能够异步处理任务队列中的作业，并实现智能重试机制。
*   **预计周期**: 2-3天

| 任务 ID | 任务名称 | 详细描述 | 状态 |
| --- | --- | --- | --- |
| **3.1** | **配置 Arq Worker** | 1. 在 `src/worker/settings.py` 中定义 `WorkerSettings`，包括Redis连接信息和任务函数列表。<br>2. 创建 `run_worker.sh` 脚本以方便地启动Worker进程。 | `to_do` |
| **3.2** | **实现任务执行逻辑** | 在 `src/worker/functions.py` 中创建核心任务函数 `execute_task`。该函数负责从数据库获取任务、更新状态，并执行（或模拟）实际业务。 | `to_do` |
| **3.3** | **实现智能重试机制** | 1. 在 `WorkerSettings` 中配置 `job_timeout` 和 `max_tries`。<br>2. 实现 `on_retry` 和 `on_job_failure` 回调函数，在任务重试或最终失败时，更新数据库中对应任务的 `status` 和 `current_retry_count`。 | `to_do` |

---

## **里程碑 4: 测试、文档与收尾**

*   **目标**: 确保项目质量，完善开发者文档，为项目交付做准备。
*   **预计周期**: 3-4天

| 任务 ID | 任务名称 | 详细描述 | 状态 |
| --- | --- | --- | --- |
| **4.1** | **单元与集成测试** | 1. 配置 `pytest` 测试框架。<br>2. 为 CRUD 业务逻辑编写单元测试。<br>3. 为所有API端点编写集成测试，验证其功能、输入校验和错误处理。 | `to_do` |
| **4.2** | **完善API文档** | 审查并优化由 FastAPI 自动生成的 OpenAPI (Swagger/ReDoc) 文档，确保其清晰、准确。 | `to_do` |
| **4.3** | **创建项目README** | 编写一份全面的 `README.md` 文件，详细说明如何配置环境、安装依赖、运行API服务器和后台Worker。 | `to_do` |
