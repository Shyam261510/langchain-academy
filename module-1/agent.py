from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm_model = ChatOpenAI(api_key=api_key, model="gpt-4o")


def multiply(a: int, b: int) -> int:
    """
    Multiply a and b
    Args:
    a:first int
    b:second int
    """
    return a * b


def add(a: int, b: int) -> int:
    """
    Add a and b
    Args:
    a:first int
    b:second int
    """
    return a + b


def divide(a: int, b: int) -> float:
    """
    Divide a and b
    Args:
    a:first int
    b:second int
    """
    return a / b


tools = [multiply, add, divide]

llm_with_tool = llm_model.bind_tools(tools, parallel_tool_calls=False)

system_prompt = SystemMessage(
    content="You are a helpful assistant whose role is to analyze the user request and perform arithmetic operations"
)


def tool_Calling_llm(state: MessagesState):
    return {"messages": llm_with_tool.invoke([system_prompt] + state["messages"])}


# Builder

builder = StateGraph(MessagesState)
memory = MemorySaver()
# Defining nodes
builder.add_node("tool_Calling_llm", tool_Calling_llm)
builder.add_node("tools", ToolNode(tools))
# Defining edges
builder.add_edge(START, "tool_Calling_llm")
builder.add_conditional_edges("tool_Calling_llm", tools_condition)
builder.add_edge("tools", "tool_Calling_llm")
# Setting Memory
graph = builder.compile(checkpointer=memory)

while True:
    user_query = input("You: ")
    messages = [HumanMessage(content=user_query)]
    # Specify a thread
    config = {"configurable": {"thread_id": "1"}}

    result = graph.invoke({"messages": messages},config)
    for message in result["messages"]:
        message.pretty_print()

    if user_query.lower() in ["byy", "quit"]:
        break
