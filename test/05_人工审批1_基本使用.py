"""
  测试5_1: 人工审批
    演示高危工具调用前的人工审批流程，支持如：删除数据库表、修改文件等 的审批流程
"""
import os

from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver # 内存检查点，用于保存中断状态
from langgraph.types import Command # 恢复执行的指令类型

load_dotenv()

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

@tool
def delete_table(table_name: str):
    """
    高危动作工具，删除传入的表
    :param table_name: 要删除的表名
    :return: 操作的返回结果
    """
    print(f"调用了delete_table工具,删除了{table_name}表!")
    return f"删除了{table_name}表！"

# 删除文件的工具
@tool
def delete_file(file_name: str):
     """
     高危动作工具，删除传入的文件
     :param file_name: 要删除的文件
     :return: 操作的返回结果
     """
     print(f"调用了delete_file工具,删除了{file_name}文件!")
     return f"删除了{file_name}文件！"

# 查询表数据的工具
@tool
def query_table(table_name: str):
     """
     查询动作工具，查询传入的表数据
     :param table_name: 要查询的表名
     :return: 查询结果
     """
     print(f"调用了query_table工具,查询了{table_name}表数据!")
     return f"查询了{table_name}表的数据！"

main_agent = create_deep_agent(
    model=llm,
    tools=[delete_table, delete_file, query_table],
    system_prompt="""回答使用中文，调用对应的工具实现对应的功能！""",
)

result = main_agent.invoke({
    "messages": [
        {"role": "user", "content": "先查询product表的数据！再删除user表，最后，删除zhaoweifeng.txt文件"}
    ]
})

print(f"--最终结果: {result['messages'][-1].content}")