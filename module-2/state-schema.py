from pydantic import BaseModel, field_validator, ValidationError
from langgraph.graph import StateGraph, START, END
from typing import Literal
import random


class PydanticState(BaseModel):
    name: str
    mood: Literal["happy", "sad"]

    @field_validator("mood")
    @classmethod
    def validated_mood(cls, value):

        if value not in ["happy", "sad"]:
            raise ValueError("Mood must be happy or sad")
        return value


def node_1(state):
    print("---Node 1---")
    return {"name": state.name + " is ... "}

def node_2(state):
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(state):
    print("---Node 3---")
    return {"mood": "sad"}


def decide_mood(state)-> Literal["node_2","node_3"]:
    return "node_2" if random.random() < 0.5 else "node_3"


try:
    ## Builder
    builder = StateGraph(PydanticState)
    ## Add node
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    ## Add edges

    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", decide_mood)
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    ## Creating graph

    graph = builder.compile()

    ## Invkoing graph

    result = graph.invoke(PydanticState(name="Shyam", mood="mad"))

    print(result)

except ValidationError as e:
    print(f"Validation Error: {e}")
