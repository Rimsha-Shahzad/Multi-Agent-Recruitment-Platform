"""
Distribution Agent
==================
Input : job_ad (from Content Agent)
Output: a list of postings across LinkedIn, Indeed, Google Jobs and the
        company careers site (mocked unless real API keys are configured
        in mock_apis.py).
"""

from mock_apis import (
    post_to_linkedin,
    post_to_indeed,
    post_to_google_jobs,
    post_to_company_site,
)


def run_distribution_agent(state: dict) -> dict:
    job_ad = state["job_ad"]
    headline = job_ad["headline"]
    body = job_ad["body"]

    postings = [
        post_to_linkedin(headline, body),
        post_to_indeed(headline, body),
        post_to_google_jobs(headline, body),
        post_to_company_site(headline, body),
    ]

    state["postings"] = postings
    state["log"].append(f"Distribution Agent: posted job ad to {len(postings)} channels.")
    return state
