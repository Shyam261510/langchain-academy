from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
import os

load_dotenv()


class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class UseMessageState(MessageState):
    pass


api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=api_key, model="gpt-4o")


def multiply(a: int, b: int) -> int:
    """Multiply a and b
    Args:
    a: fist int
    b: second int
    """

    return a * b


llm_with_tools = llm.bind_tools([multiply])

inital_prompt = [
    SystemMessage(content="Hello! How can I assist you?"),
    HumanMessage(content="I'm looking for information on marine biology"),
]

new_message = AIMessage(content="Sure, I can help with that. What specifically are you interested in?")

add_messages(inital_prompt, new_message)


def tool_calling_llm(state: MessageState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build graph

builder = StateGraph(MessageState)

builder.add_node("tool_calling_llm", tool_calling_llm)

builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)

graph = builder.compile()

final_result = graph.invoke({"messages": HumanMessage(content="Hello!")})

# results = llm_with_tools.invoke([HumanMessage(content=f"What is 2 multiplied by 3")])

print("Final State:", final_result.get("messages"))
