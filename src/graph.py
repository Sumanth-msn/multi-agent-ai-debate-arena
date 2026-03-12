import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.tools import web_search
from src.agents import run_for_agent, run_against_agent, run_judge_agent


# -------------------------
# State Schema
# -------------------------


class DebateState(TypedDict):
    topic: str
    search_results: str
    for_argument: str
    against_argument: str
    verdict: str
    error: str


# -------------------------
# Nodes
# -------------------------


def search_node(state: DebateState) -> DebateState:
    """Search web for facts about the topic before debate starts."""
    print("📡 Searching web for context...")
    try:
        results = web_search.invoke(state["topic"])
        state["search_results"] = results
        state["error"] = ""
    except Exception as e:
        state["search_results"] = "No search results available."
        state["error"] = str(e)
    return state


def for_agent_node(state: DebateState) -> DebateState:
    """Agent that argues FOR the topic."""
    print("🟢 FOR agent building argument...")
    try:
        argument = run_for_agent(state["topic"], state["search_results"])
        state["for_argument"] = argument
    except Exception as e:
        state["for_argument"] = "FOR agent failed."
        state["error"] = str(e)
    return state


def against_agent_node(state: DebateState) -> DebateState:
    """Agent that argues AGAINST the topic."""
    print("🔴 AGAINST agent building argument...")
    try:
        argument = run_against_agent(state["topic"], state["search_results"])
        state["against_argument"] = argument
    except Exception as e:
        state["against_argument"] = "AGAINST agent failed."
        state["error"] = str(e)
    return state


def judge_node(state: DebateState) -> DebateState:
    """Judge agent evaluates both sides and gives verdict."""
    print("⚖️  Judge evaluating arguments...")
    try:
        verdict = run_judge_agent(
            state["topic"], state["for_argument"], state["against_argument"]
        )
        state["verdict"] = verdict
    except Exception as e:
        state["verdict"] = "Judge failed to evaluate."
        state["error"] = str(e)
    return state


# -------------------------
# Build Graph
# -------------------------


def build_graph():
    workflow = StateGraph(DebateState)

    # Add nodes
    workflow.add_node("search", search_node)
    workflow.add_node("for_agent", for_agent_node)
    workflow.add_node("against_agent", against_agent_node)
    workflow.add_node("judge", judge_node)

    # Define flow
    workflow.set_entry_point("search")
    workflow.add_edge("search", "for_agent")
    workflow.add_edge("for_agent", "against_agent")
    workflow.add_edge("against_agent", "judge")
    workflow.add_edge("judge", END)

    return workflow.compile()


# -------------------------
# Public Runner
# -------------------------

debate_app = build_graph()


def run_debate(topic: str) -> DebateState:
    """Run the full debate pipeline and return final state."""
    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    initial_state: DebateState = {
        "topic": topic.strip(),
        "search_results": "",
        "for_argument": "",
        "against_argument": "",
        "verdict": "",
        "error": "",
    }

    return debate_app.invoke(initial_state)
