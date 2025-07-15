# ai_workflow - AI 驱动的开发工作流演示

**欢迎来到 `ai_workflow` 项目！**

这个仓库的核心目的**不是**提供一个可用的任务管理工具，而是作为一个透明的、可追溯的案例，完整展示一个**由 AI 助手驱动的软件开发工作流**。

仓库中的所有内容，从需求文档到最终代码，都是通过与 AI 助手（如 Gemini CLI）的交互逐步生成的。它是一个研究和演示“人机协作”开发模式的活样本。

---

## 核心理念：过程即产品

在这个项目中，真正的“产品”是开发过程本身。代码 (`src/`) 只是这个过程的最终产物。我们关注的焦点是那些指导、记录和塑造了最终代码的**工作流构件 (Workflow Artifacts)**。

以下是这些核心构件的导览，建议您按顺序阅读，以完整理解整个工作流：

### 1. 需求与顶层设计 (`/docs`)

这里是项目的起点，定义了“我们要做什么”和“我们打算怎么做”。

-   `docs/product_requirement_docs.md`: **产品需求文档 (PRD)**。描述了项目的目标、核心功能和用户画像，是一切的开端。
-   `docs/architecture.md`: **架构设计文档**。基于需求，勾勒出系统的技术蓝图，包括组件图、流程图和技术选型。
-   `docs/technical.md`: **技术细节文档**。对架构中的关键技术点进行更深入的阐述。

### 2. AI 交互规则与上下文 (`/.cursor/rules`)

为了让 AI 助手能高效、准确地执行任务，我们为其设定了一系列规则和上下文。

-   `rules/`: 这个目录下的 `.mdc` 文件定义了 AI 在执行特定任务（如调试、规划、实现）时应遵循的指导方针和约束。这相当于给 AI 的“操作手册”。

### 3. 任务规划与执行日志 (`/tasks`)

这里将高层设计分解为具体的、可执行的步骤。

-   `tasks/tasks_plan.md`: **任务执行计划**。这是将架构蓝图转化为具体开发步骤的清单，是 AI 执行编码任务的路线图。
-   `tasks/changelog.md`: **变更日志**。记录了项目在开发过程中的主要变更和决策。

### 4. 工作流元文档 (`/workflow_docs`)

这里包含了关于工作流本身的思考和记录。

-   `workflow_docs/01-plan-phase.md`: 描述了规划阶段的详细思考过程。
-   `workflow_docs/cursor_.md`: 记录了与特定工具（Cursor）或 AI 交互时的笔记和经验。

### 5. AI 对话历史 (Git Commits & Chat Logs)

我们与 AI 的大部分交互都体现在 Git 的提交历史中。每一次 `git commit` 都代表了���次具体的、由 AI 完成的任务。建议查看 commit messages 来理解每一步的意图。

---

## 工作流的最终产物：一个可运行的应用

遵循上述工作流，我们最终生成了一个 FastAPI 应用。您可以运行它来验证该工作流确实产出了一个有效的、可工作的软件。

### 如何运行和验证

1.  **环境准备与安装**:
    -   确保 Docker 已安装并运行。
    -   克隆仓库，创建并激活 Python 虚拟环境 (`python -m venv venv && source venv/bin/activate`)。
    -   安装依赖: `pip install -r requirements.txt`。

2.  **启动依赖服务**:
    ```bash
    # 启动 MySQL 和 Redis 容器
    docker run -d --name mysql-taskzen -p 3306:3306 -e MYSQL_ROOT_PASSWORD=your_password -e MYSQL_DATABASE=task_zen_db mysql:8
    docker run -d --name redis-taskzen -p 6379:6379 redis:7
    ```

3.  **配置与迁移**:
    -   在根目录创建 `.env` 文件（可参考 `src/core/config.py`）。
    -   运行数据库迁移: `alembic upgrade head`。

4.  **启动并观察**:
    -   **终端 1 (API Server)**: `uvicorn src.main:app --reload`
    -   **终端 2 (Worker)**: `sh ./run_worker.sh`
    -   访问 `http://localhost:8000/docs`，按照上一版 README 中的演示步骤创建一个任务，观察两个终端的日志输出，亲身体验这个由 AI 构建的系统的内部流转。
