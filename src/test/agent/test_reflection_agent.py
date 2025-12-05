from llm.hello_agent_llm import HelloAgentsLLM
from agent.reflection.reflection_agent import ReflectionAgent


def test_reflection_agent(config, options):
    task = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)。"

    llm_client = HelloAgentsLLM(config, options)
    agent = ReflectionAgent(config, options, llm_client)
    agent.run(task)
