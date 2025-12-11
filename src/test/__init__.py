from pyouter import Router


def dispatch():
    """ 测试路由

    """

    from test.llm.test_hello_agent_llm import test_hello_agent_llm
    from test.tools.test_search import test_search
    from test.agent.test_react_agent import test_react_agent
    from test.agent.test_plan_and_solve_agent import test_plan_and_solve_agent
    from test.agent.test_reflection_agent import test_reflection_agent
    from test.agent.test_langgraph_agent import test_dialogue_system
    from test.agent.test_autogen_agent import test_software_team

    router = Router(
        llm = Router(
            hello_agent = test_hello_agent_llm
        ),
        tools = Router(
            search = test_search
        ),
        agent = Router(
            react = test_react_agent,
            plan_and_solve = test_plan_and_solve_agent,
            reflection = test_reflection_agent,
            langgraph = Router(
                dialogue_system = test_dialogue_system
            ),
            autogen = Router(
                software_team = test_software_team
            )
        )
    )

    return router