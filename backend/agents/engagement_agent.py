"""
Engagement Agent
================
Input : postings (from Distribution Agent) + persona
Output: a pool of candidate leads, each nurtured with a personalised
        outreach message (sent via HubSpot, mocked unless HUBSPOT_API_KEY
        is configured).
"""

import random
from mock_apis import call_llm, send_nurture_message_via_hubspot

FIRST_NAMES = ["Amina", "Bilal", "Sara", "Hamza", "Ayesha", "Usman", "Zara", "Ali", "Mehak", "Fahad"]
LAST_NAMES = ["Khan", "Ahmed", "Malik", "Raza", "Iqbal", "Sheikh", "Hussain", "Farooq", "Javed", "Qureshi"]

SYSTEM_PROMPT = """You are a friendly recruitment outreach specialist.
Write a short (2-3 sentence), warm, personalised nurture message for a
cold candidate lead, referencing the role and the company. Respond with
plain text only, no JSON."""


def _mock_message(lead_name: str, job_title: str, company: str):
    first = lead_name.split()[0]
    return (
        f"Hi {first}, your background caught our eye for the {job_title} role at {company}. "
        f"We think you'd be a great fit and would love to chat about what we're building — "
        f"are you open to a quick intro call this week?"
    )


def _generate_leads(num_leads: int, source_channels: list[str]):
    leads = []
    for _ in range(num_leads):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        leads.append({
            "name": name,
            "source": random.choice(source_channels),
            "fit_score": round(random.uniform(0.55, 0.97), 2),
        })
    return leads


def run_engagement_agent(state: dict) -> dict:
    job_title = state["job_title"]
    company = state["company"]
    postings = state["postings"]
    channels = [p["channel"] for p in postings]

    # Simulate cold leads sourced from the postings (e.g. profile search / applicants)
    num_leads = random.randint(6, 10)
    leads = _generate_leads(num_leads, channels)

    for lead in leads:
        user_prompt = f"Lead name: {lead['name']}\nRole: {job_title}\nCompany: {company}"
        raw = call_llm(SYSTEM_PROMPT, user_prompt)
        message = raw if raw else _mock_message(lead["name"], job_title, company)

        result = send_nurture_message_via_hubspot(lead["name"], message)

        lead["last_message"] = message
        lead["status"] = "Nurturing" if lead["fit_score"] >= 0.65 else "New"
        if lead["fit_score"] >= 0.85:
            lead["status"] = "Engaged"

    state["leads"] = leads
    state["log"].append(f"Engagement Agent: generated and nurtured {len(leads)} candidate leads.")
    return state
