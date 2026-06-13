"""
LangGraph Workflow
==================
Wires the 5 agents into a linear pipeline:

  Persona Agent -> Content Agent -> Distribution Agent
      -> Engagement Agent -> Analytics Agent -> END

Each agent reads/writes a shared `PipelineState` dict. This is the
core "Agent Workflow" described in the project brief.
"""

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

from agents.persona_agent import run_persona_agent
from agents.content_agent import run_content_agent
from agents.distribution_agent import run_distribution_agent
from agents.engagement_agent import run_engagement_agent
from agents.analytics_agent import run_analytics_agent


class PipelineState(TypedDict, total=False):
    job_title: str
    company: str
    location: str
    seniority: str
    persona: Dict[str, Any]
    job_ad: Dict[str, Any]
    postings: List[Dict[str, Any]]
    leads: List[Dict[str, Any]]
    analytics: Dict[str, Any]
    log: List[str]


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("persona_agent", run_persona_agent)
    graph.add_node("content_agent", run_content_agent)
    graph.add_node("distribution_agent", run_distribution_agent)
    graph.add_node("engagement_agent", run_engagement_agent)
    graph.add_node("analytics_agent", run_analytics_agent)

    graph.set_entry_point("persona_agent")
    graph.add_edge("persona_agent", "content_agent")
    graph.add_edge("content_agent", "distribution_agent")
    graph.add_edge("distribution_agent", "engagement_agent")
    graph.add_edge("engagement_agent", "analytics_agent")
    graph.add_edge("analytics_agent", END)

    return graph.compile()


def run_pipeline(job_title: str, company: str, location: str, seniority: str = "Mid-level") -> PipelineState:
    app = build_graph()
    initial_state: PipelineState = {
        "job_title": job_title,
        "company": company,
        "location": location,
        "seniority": seniority,
        "log": [],
    }
    final_state = app.invoke(initial_state)
    return final_state
