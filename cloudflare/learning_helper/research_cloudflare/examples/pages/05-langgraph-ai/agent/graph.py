"""
The LangGraph agent: one LLM node, one tool node, one conditional edge.

State:
    messages: list[BaseMessage]  (LangGraph appends with add_messages)

Nodes:
    llm    -> call ChatAnthropic with the calculator tool bound
    tools  -> ToolNode runs the requested tool and appends a ToolMessage

Edges:
    START -> llm
    llm   -> tools  (if the LLM response contains a tool_call)
    llm   -> END    (otherwise)
    tools -> llm    (always, so the LLM can write a final answer)
"""
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage


# ---------- Tool ----------

def calculator(expression: str) -> str:
    """Evaluate a math expression safely. Supports + - * / and parentheses.

    Uses ast.parse rather than eval() so arbitrary Python is rejected.
    """
    import ast
    import operator

    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ops:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            return ops[op_type](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -_eval(node.operand)
        raise ValueError("Only numbers and + - * / are allowed.")

    tree = ast.parse(expression, mode="eval")
    return str(_eval(tree.body))


# ---------- State ----------

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ---------- Model ----------

TOOLS = [calculator]
# claude-haiku-4-5 is fast and cheap; great default for an example.
# Swap to claude-sonnet-4-5 for higher-quality answers.
LLM = ChatAnthropic(model="claude-haiku-4-5", temperature=0).bind_tools(TOOLS)


# ---------- Nodes ----------

def llm_node(state: State) -> dict:
    """Call the LLM with the current message history."""
    response = LLM.invoke(state["messages"])
    return {"messages": [response]}


# ---------- Graph ----------

_builder = StateGraph(State)
_builder.add_node("llm", llm_node)
_builder.add_node("tools", ToolNode(TOOLS))
_builder.add_edge(START, "llm")
_builder.add_conditional_edges("llm", tools_condition)
_builder.add_edge("tools", "llm")

# In-memory checkpointer so the same thread_id keeps a conversation history.
_memory = InMemorySaver()
GRAPH = _builder.compile(checkpointer=_memory)


# ---------- Public API ----------

def chat(message: str, thread_id: str = "default-user") -> str:
    """Send a user message; return the agent's final text reply.

    Loops over streamed events internally so a multi-step tool call
    (e.g. "compute (12+8)*3, then add 100") returns once the LLM
    has produced a final answer, not an intermediate tool_call message.
    """
    config = {"configurable": {"thread_id": thread_id}}
    events = GRAPH.stream(
        {"messages": [HumanMessage(content=message)]},
        config=config,
        stream_mode="values",
    )

    final_text = ""
    for event in events:
        # event is a dict with the latest state; grab the last message.
        msgs = event.get("messages", [])
        if not msgs:
            continue
        last = msgs[-1]
        # Only keep plain AI text replies; skip tool calls and tool results.
        if isinstance(last, AIMessage) and not getattr(last, "tool_calls", []):
            final_text = last.content if isinstance(last.content, str) else str(last.content)

    return final_text or "(no reply)"