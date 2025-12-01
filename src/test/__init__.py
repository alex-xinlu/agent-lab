from pyouter import Router


def dispatch():
    """ 测试路由

    """

    from test.llm.test_hello_agent_llm import test_hello_agent_llm

    router = Router(
        llm = Router(
            hello_agent = test_hello_agent_llm
        )
    )

    return router