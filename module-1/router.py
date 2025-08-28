from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


def multiply(a: int, b: int) -> int:
    """Multiply a and b
    Args:
    a: fist int
    b: second int
    """

    return a * b


def add(a: int, b: int) -> int:
    """ADD a and b
    Args:
    a: fist int
    b: second int
    """

    return a + b


api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=api_key, model="gpt-4o")

llm_with_tools = llm.bind_tools([multiply, add])


def tool_calling_LLm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build Graph

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_LLm", tool_calling_LLm)
builder.add_node("tools", ToolNode([multiply, add]))
builder.add_edge(START, "tool_calling_LLm")
builder.add_conditional_edges(
    "tool_calling_LLm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()

messages = [HumanMessage(content="Hello, How's going? What is the sum of 7 and 13 ?")]
messages = graph.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()
