from typing import TypedDict, Dict

class GraphState(TypedDict):
    question: str
    answer: str
    route: str
    memory: Dict