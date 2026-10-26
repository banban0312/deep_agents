"""
  测试06_3: 演示使用CompositeBackend实现长期记忆
 	不同路由采用不同的存储方案
"""
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend, FilesystemBackend, CompositeBackend
from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os
from pathlib import Path

load_dotenv()

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

agent = create_deep_agent(
    model=llm,
    tools=[],
    system_prompt="""你是一个智能助手。
    - 普通文件：直接写入文件名（如 `report.txt`），保存到本地工作区。
    - 重要记忆：写入 `/store/` 目录（如 `/store/profile.txt`），保存到store指定的存储方式中。
    """
)

# 运行 Agent 测试
config = {"configurable": {"thread_id": "thread_composite"}}

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """1. 创建文件 local.txt，内容'本地文件内容数据...'。
                      2. 创建文件 /store/memory，内容'重要记忆数据...'。"""
    }]
}, config=config)

print("Agent 回复:", result["messages"][-1].content)