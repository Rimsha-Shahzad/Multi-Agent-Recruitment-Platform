"""
Analytics Agent
===============
Input : postings + leads
Output: aggregated pipeline metrics (impressions, clicks, applications,
         qualified leads, interviews, hires, CTR, application rate).

In a production system these numbers would come from each channel's
reporting API plus your ATS/CRM. Here they are simulated based on the
number of channels and leads so the dashboard has realistic figures to
show end-to-end.
"""

import random


def run_analytics_agent(state: dict) -> dict:
    postings = state["postings"]
    leads = state["leads"]

    channels_count = len(postings)
    impressions = random.randint(800, 1500) * channels_count
    clicks = int(impressions * random.uniform(0.04, 0.09))
    applications = int(clicks * random.uniform(0.08, 0.18))

    qualified_leads = len([l for l in leads if l["fit_score"] >= 0.65])
    interviews = len([l for l in leads if l["status"] == "Engaged"])
    hires = 1 if interviews and random.random() > 0.5 else 0

    analytics = {
        "impressions": impressions,
        "clicks": clicks,
        "applications": applications,
        "qualified_leads": qualified_leads,
        "interviews": interviews,
        "hires": hires,
        "click_through_rate": round((clicks / impressions) * 100, 2) if impressions else 0,
        "application_rate": round((applications / clicks) * 100, 2) if clicks else 0,
    }

    state["analytics"] = analytics
    state["log"].append("Analytics Agent: computed pipeline metrics.")
    return state
