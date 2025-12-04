# agent-lab

## 简介
该项目主要用于 agent 的学习、实验与探索

## 目录结构说明
* src/chat: prompt 工程相关任务或功能
* src/common: 公共组建，例如：日志、实用函数等
* src/config: 项目配置
* src/data: 测试数据目录 (不提交) 
* src/tools: agent 需要用到的工具
* src/agent: 搭建的 agent
* src/component: 基础组件
* src/llm: 提供 llm API 接口
* src/test: 功能测试模块

## 运行命令说明
该项目使用 [pyouter](https://github.com/fanfeilong/pyouter) 框架进行组织，所有功能将在一个树状结构中进行管理。程序入口函数为 `./src/main.py`

pyouter 介绍博客：
* [项目框架管理工具pyouter的实践](https://blog.csdn.net/qq_43576728/article/details/140461789)
* [开源小项目：pyouter 0.0.1 发布](https://blog.csdn.net/huanhuilong/article/details/121481377)

命令示例：`python main.py agent_lab.test.agent.react`，测试 ReAct agent，其中 `agent_lab.test.agent.react` 解释如下：
* agent_lab: 项目根结点
* test: 表示这是一项功能测试
* agent: 表示这是一个 agent
* react: 表示这是 ReAct agent

若要查看所有支持的命令，可执行 `python main.py chat -i` 进行打印，如下所示。
其中的 action 就是树状结构的叶子结点，也就是所有可执行的功能，具体如下所示 (2025-12-03 打印)：
```
[pyouter] ->router2: agent_lab
[pyouter]   ->router2: agent_lab.test
[pyouter]   ->router2: agent_lab.test
[pyouter]   ->router2: agent_lab.test
[pyouter]     ->router2: agent_lab.test.llm
[pyouter]     ->router2: agent_lab.test.tools
[pyouter]     ->router2: agent_lab.test.agent
[pyouter]       ->action: agent_lab.test.llm.hello_agent
[pyouter]       ->action: agent_lab.test.tools.search
[pyouter]       ->action: agent_lab.test.agent.react
```

## 当前支持的 agent（范式）
- [x] ReAct

## 当前支持的工具
- [x] search: SerpApi
- [x] time: get_current_date

## 注意
需要在项目的根目录下，根据 `.env.example` 配置 `.env` 文件中的参数（`.env` 文件自行在项目根目录下新建）。