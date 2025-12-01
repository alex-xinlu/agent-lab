from llm.hello_agent_llm import HelloAgentsLLM


def test_hello_agent_llm(config, options):
    llmClient = HelloAgentsLLM(config, options)
    
    exampleMessages = [
        {"role": "system", "content": "You are a helpful assistant that writes Python code."},
        {"role": "user", "content": "写一个快速排序算法"}
    ]
    
    print("--- 调用LLM ---")
    responseText = llmClient.think(exampleMessages)
    if responseText:
        print("\n\n--- 完整模型响应 ---")
        print(responseText)