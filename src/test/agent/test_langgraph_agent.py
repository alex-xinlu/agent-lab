import asyncio

from agent.langgraph.dialogue_system.dialogue_system import dialogue_system_run


def test_dialogue_system(config, options):
    asyncio.run(dialogue_system_run())

