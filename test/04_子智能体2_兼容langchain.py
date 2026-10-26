"""
  测试4_2: 兼容langchain子智能体格式
"""
import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model


load_dotenv()

chat_model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)


# 创建主智能体，设置子智能体
main_agent = create_deep_agent(
    model=chat_model,
    subagents=[],
    system_prompt="你是一个智能助手，所有的业务动作，你不要亲自做，都找子智能体进行处理！"
)

print("====开始执行任务====")
result = main_agent.invoke({
    "messages": [
        {"role": "user", "content": "武汉今天的天气怎么样？"}
    ]
})
print(f"最终结果：{result['messages'][-1].content}")