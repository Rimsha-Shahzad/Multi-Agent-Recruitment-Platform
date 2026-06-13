"""
Persona Agent
=============
Input : job title, company, location, seniority
Output: a structured "ideal candidate" persona that downstream agents
        (Content, Distribution, Engagement) use to tailor their work.
"""

from mock_apis import call_llm, safe_json_loads

SYSTEM_PROMPT = """You are a senior recruitment marketing strategist.
Given a role, build a structured ideal-candidate persona.
Respond ONLY with valid JSON using exactly these keys:
title, summary, must_have_skills (list), nice_to_have_skills (list),
experience_years (string), motivations (list), preferred_channels (list),
keywords (list of 5-8 SEO/search keywords for job ads)."""


def _mock_persona(job_title: str, company: str, location: str, seniority: str):
    return {
        "title": f"{seniority} {job_title}",
        "summary": (
            f"A {seniority.lower()} {job_title} based in or willing to work from {location}, "
            f"who is excited about joining {company}'s mission, enjoys solving real-world problems, "
            f"and is looking for a role with growth, autonomy, and modern tooling."
        ),
        "must_have_skills": ["Core technical skills for the role", "Communication", "Collaboration"],
        "nice_to_have_skills": ["Startup/scale-up experience", "Cross-functional project work"],
        "experience_years": "3-6 years" if seniority.lower() == "mid-level" else "1-3 years"
        if seniority.lower() == "junior" else "7+ years",
        "motivations": ["Career growth", "Meaningful impact", "Flexible/hybrid work", "Competitive pay"],
        "preferred_channels": ["LinkedIn", "Indeed", "Google Jobs", "Referrals"],
        "keywords": [job_title, company, location, seniority, "remote", "career growth"],
    }


def run_persona_agent(state: dict) -> dict:
    job_title = state["job_title"]
    company = state["company"]
    location = state["location"]
    seniority = state.get("seniority", "Mid-level")

    user_prompt = (
        f"Role: {job_title}\nCompany: {company}\nLocation: {location}\nSeniority: {seniority}"
    )

    raw = call_llm(SYSTEM_PROMPT, user_prompt, json_mode=True)
    persona = safe_json_loads(raw, _mock_persona(job_title, company, location, seniority))

    state["persona"] = persona
    state["log"].append("Persona Agent: built ideal-candidate persona.")
    return state
