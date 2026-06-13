"""
Content Agent
=============
Input : persona (from Persona Agent) + job details
Output: headline, body copy, and call-to-action for the job ad,
        written to appeal to the persona's motivations.
"""

from mock_apis import call_llm, safe_json_loads

SYSTEM_PROMPT = """You are an expert recruitment copywriter.
Given a job and a candidate persona, write a compelling job advertisement.
Respond ONLY with valid JSON using exactly these keys:
headline (string, under 100 chars), body (string, 3-5 short paragraphs,
plain text with \\n\\n between paragraphs), call_to_action (string)."""


def _mock_job_ad(job_title: str, company: str, location: str, persona: dict):
    motivations = ", ".join(persona.get("motivations", [])[:3])
    skills = ", ".join(persona.get("must_have_skills", [])[:3])
    headline = f"{job_title} at {company} — {location} (Hiring Now)"
    body = (
        f"{company} is looking for a {persona.get('title', job_title)} to join our team in {location}.\n\n"
        f"You'll work on impactful projects while growing your skills in {skills}. "
        f"We offer {motivations}, and a culture that values your contributions from day one.\n\n"
        f"If you're driven by {persona.get('motivations', ['growth'])[0].lower()} and want to make "
        f"a real impact, we'd love to hear from you."
    )
    cta = f"Apply now to become {company}'s next {job_title}."
    return {"headline": headline, "body": body, "call_to_action": cta}


def run_content_agent(state: dict) -> dict:
    job_title = state["job_title"]
    company = state["company"]
    location = state["location"]
    persona = state["persona"]

    user_prompt = (
        f"Job title: {job_title}\nCompany: {company}\nLocation: {location}\n"
        f"Candidate persona: {persona}"
    )

    raw = call_llm(SYSTEM_PROMPT, user_prompt, json_mode=True)
    job_ad = safe_json_loads(raw, _mock_job_ad(job_title, company, location, persona))

    state["job_ad"] = job_ad
    state["log"].append("Content Agent: generated job ad copy.")
    return state
