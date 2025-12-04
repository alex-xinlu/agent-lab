from llm.hello_agent_llm import HelloAgentsLLM
from agent.plan_and_solve.plan_and_solve_agent import PlanAndSolveAgent


def test_plan_and_solve_agent(config, options):
    question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"

    llm_client = HelloAgentsLLM(config, options)
    agent = PlanAndSolveAgent(config, options, llm_client)
    agent.run(question)