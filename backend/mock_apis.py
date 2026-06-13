"""
External integrations layer.

Every function here checks whether a matching API key exists in the
environment. If it does, you can extend the function to make a real call.
If it doesn't, a realistic MOCK response is returned so the rest of the
pipeline (and the LangGraph workflow) works end-to-end without any paid
accounts. This lets you DEMO the full agent workflow today, then swap in
real credentials later without changing any agent logic.
"""

import os
import random
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
INDEED_API_KEY = os.getenv("INDEED_API_KEY")
GOOGLE_JOBS_API_KEY = os.getenv("GOOGLE_JOBS_API_KEY")
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")


# ---------------------------------------------------------------------------
# LLM (GPT-4o)
# ---------------------------------------------------------------------------
def call_llm(system_prompt: str, user_prompt: str, json_mode: bool = False):
    """
    Calls GPT-4o if OPENAI_API_KEY is set. Otherwise returns None so the
    calling agent can fall back to its own mock generator.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            **kwargs,
        )
        return response.choices[0].message.content
    except Exception as exc:  # pragma: no cover - network/key issues
        print(f"[LLM] Falling back to mock generator due to error: {exc}")
        return None


# ---------------------------------------------------------------------------
# Distribution channels
# ---------------------------------------------------------------------------
def post_to_linkedin(headline: str, body: str):
    if LINKEDIN_API_KEY:
        # TODO: real call to LinkedIn Job Postings API would go here
        pass
    return {
        "channel": "LinkedIn",
        "status": "posted",
        "external_url": f"https://www.linkedin.com/jobs/view/mock-{random.randint(100000, 999999)}",
    }


def post_to_indeed(headline: str, body: str):
    if INDEED_API_KEY:
        # TODO: real call to Indeed Apply/Publisher API would go here
        pass
    return {
        "channel": "Indeed",
        "status": "posted",
        "external_url": f"https://www.indeed.com/viewjob?jk=mock{random.randint(100000, 999999)}",
    }


def post_to_google_jobs(headline: str, body: str):
    if GOOGLE_JOBS_API_KEY:
        # TODO: real call to Google for Jobs (via JobPosting structured data) would go here
        pass
    return {
        "channel": "Google Jobs",
        "status": "posted",
        "external_url": f"https://www.google.com/search?q=mock+job+{random.randint(100000, 999999)}",
    }


def post_to_company_site(headline: str, body: str):
    return {
        "channel": "Company Careers Site",
        "status": "posted",
        "external_url": f"https://careers.example.com/jobs/mock-{random.randint(100000, 999999)}",
    }


# ---------------------------------------------------------------------------
# Engagement / CRM (HubSpot)
# ---------------------------------------------------------------------------
def send_nurture_message_via_hubspot(lead_name: str, message: str):
    if HUBSPOT_API_KEY:
        # TODO: real call to HubSpot Marketing/CRM API would go here
        pass
    return {"lead": lead_name, "status": "queued", "channel": "HubSpot Email Sequence"}


# ---------------------------------------------------------------------------
# Helper: safe JSON parsing of LLM output
# ---------------------------------------------------------------------------
def safe_json_loads(raw, fallback):
    if not raw:
        return fallback
    try:
        # Strip markdown code fences if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.replace("json\n", "", 1).replace("json", "", 1)
        return json.loads(cleaned)
    except Exception:
        return fallback
