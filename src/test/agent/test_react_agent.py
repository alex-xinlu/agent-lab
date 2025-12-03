from tools.tool_executor import ToolExecutor
from tools.search.search import search
from tools.time.time import get_current_date
from agent.react.react_agent import ReActAgent
from llm.hello_agent_llm import HelloAgentsLLM


def test_react_agent(config, options):
    # 1. 初始化工具执行器
    tool_executor = ToolExecutor()

    # 2. 注册工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.register_tool("Search", search_description, search)
    date_description = "获取当前的日期，格式为`%Y-%m-%d`。当你不确定当前时间时，应使用此工具。"
    tool_executor.register_tool("Date", date_description, get_current_date)

    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(tool_executor.get_available_tools())

    # 4. 初始化语言模型
    llm_client = HelloAgentsLLM(config, options)

    # 5. 调用 ReAct agent
    react_agent = ReActAgent(llm_client, tool_executor)
    question = "华为最新手机型号及主要卖点"
    react_agent.run(question)
