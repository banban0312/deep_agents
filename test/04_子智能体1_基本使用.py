"""
测试4_1: 子智能体的基本使用  => 基于字典定义子agent
创建一个主智能体，它拥有三个助手：
    1.  **天气助手**：查询天气（固定返回“晴朗”）。
    2.  **计算助手**：处理数学问题。
    3.  **翻译助手**：负责中英互译。
"""

import os
from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 加载.env配置
load_dotenv()

# 初始化模型
llm=init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
)

# 创建深度代理
agent = create_deep_agent(
    model = llm,
    system_prompt="你是一个强大的助手",
    tools=[],
)

def query_stream(query: str):
    for chunk in agent.stream({
        "messages": [{"role": "user", "content": query}]
    }):
        # print(chunk)
        for key, value in chunk.items():
            if key in ["tools", "model"]:
                message = value["messages"][0]
                if key=="model": # 模型处理返回
                    tool_calls = message.tool_calls # 要调用的工具列表
                    if tool_calls: # tool_calls有值，说明准备调用工具
                        for tool_call in tool_calls:
                            print(f"--模型返回，决定调用工具【{tool_call['name']}】,参数为：{tool_call['args']}")
                    else: # 如果没有，说明是模块返回的最终结果
                        print(f"--模型返回，最终结果：{message.content}")
                elif key=="tools": # 工具处理返回
                    name = message.name # 工具名
                    content = message.content # 结果数据
                    print(f"-- 工具[{name}]执行返回结果：{content}")

if __name__ == '__main__':
    query_stream("今天武汉天气怎么样? 再计算123+234-99等于几？，同时将'好好学习，天天向上'翻译为英文")
