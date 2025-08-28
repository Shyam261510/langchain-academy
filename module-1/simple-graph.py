import random
from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    graph_state: str


def node_1(state: State) -> State:
    print("---NODE1---")
    return {"graph_state": state["graph_state"] + "I am"}


def node_2(state: State) -> State:
    print("---NODE2---")
    return {"graph_state": state["graph_state"] + " happy! 😄"}


def node_3(state: State) -> State:
    print("---NODE3---")
    return {"graph_state": state["graph_state"] + " Sad! 😔"}


def decide_mood(state: State) -> Literal["node_2", "node_3"]:

    random_number = random.random()
    # 50% of the time, we return Node 2
    if random_number < 0.5:
        return "node_2"

    # 50% of the time, we return Node 3
    return "node_3"


# Build graph

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add

graph = builder.compile()

# Run the graph
final_state = graph.invoke({"graph_state": "Hello I am Shyam sharma. "})
print("Final State:", final_state.get("graph_state"))
