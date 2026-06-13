"""
FastAPI backend for the AI-Powered Recruitment Marketing Platform.

Run with:
    uvicorn main:app --reload --port 8000

Endpoints:
    POST /api/campaigns/run   -> runs the full 5-agent LangGraph pipeline
    GET  /api/campaigns       -> list all campaigns (most recent first)
    GET  /api/campaigns/{id}  -> full detail for one campaign
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db, init_db, SessionLocal
import models
from graph import run_pipeline

app = FastAPI(title="AI-Powered Recruitment Marketing Platform")

# Allow the Next.js dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


class CampaignRequest(BaseModel):
    job_title: str
    company: str
    location: str
    seniority: str = "Mid-level"


@app.post("/api/campaigns/run")
def run_campaign(payload: CampaignRequest, db: Session = Depends(get_db)):
    # 1. Run the LangGraph multi-agent pipeline
    result = run_pipeline(
        job_title=payload.job_title,
        company=payload.company,
        location=payload.location,
        seniority=payload.seniority,
    )

    # 2. Persist everything to the database
    campaign = models.Campaign(
        job_title=payload.job_title,
        company=payload.company,
        location=payload.location,
        seniority=payload.seniority,
        status="completed",
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    persona = result["persona"]
    db.add(models.Persona(
        campaign_id=campaign.id,
        title=persona.get("title"),
        summary=persona.get("summary"),
        must_have_skills=persona.get("must_have_skills"),
        nice_to_have_skills=persona.get("nice_to_have_skills"),
        experience_years=persona.get("experience_years"),
        motivations=persona.get("motivations"),
        preferred_channels=persona.get("preferred_channels"),
        keywords=persona.get("keywords"),
    ))

    job_ad = result["job_ad"]
    db.add(models.JobAd(
        campaign_id=campaign.id,
        headline=job_ad.get("headline"),
        body=job_ad.get("body"),
        call_to_action=job_ad.get("call_to_action"),
    ))

    for posting in result["postings"]:
        db.add(models.Posting(
            campaign_id=campaign.id,
            channel=posting["channel"],
            status=posting["status"],
            external_url=posting["external_url"],
        ))

    for lead in result["leads"]:
        db.add(models.Lead(
            campaign_id=campaign.id,
            name=lead["name"],
            source=lead["source"],
            fit_score=lead["fit_score"],
            status=lead["status"],
            last_message=lead["last_message"],
        ))

    analytics = result["analytics"]
    db.add(models.AnalyticsSnapshot(
        campaign_id=campaign.id,
        impressions=analytics["impressions"],
        clicks=analytics["clicks"],
        applications=analytics["applications"],
        qualified_leads=analytics["qualified_leads"],
        interviews=analytics["interviews"],
        hires=analytics["hires"],
        click_through_rate=analytics["click_through_rate"],
        application_rate=analytics["application_rate"],
    ))

    db.commit()

    return {
        "campaign_id": campaign.id,
        "log": result["log"],
        "persona": persona,
        "job_ad": job_ad,
        "postings": result["postings"],
        "leads": result["leads"],
        "analytics": analytics,
    }


@app.get("/api/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(models.Campaign).order_by(models.Campaign.id.desc()).all()
    return [
        {
            "id": c.id,
            "job_title": c.job_title,
            "company": c.company,
            "location": c.location,
            "seniority": c.seniority,
            "status": c.status,
            "created_at": c.created_at,
        }
        for c in campaigns
    ]


@app.get("/api/campaigns/{campaign_id}")
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    persona = campaign.persona
    job_ad = campaign.job_ad
    analytics = campaign.analytics

    return {
        "id": campaign.id,
        "job_title": campaign.job_title,
        "company": campaign.company,
        "location": campaign.location,
        "seniority": campaign.seniority,
        "status": campaign.status,
        "created_at": campaign.created_at,
        "persona": {
            "title": persona.title,
            "summary": persona.summary,
            "must_have_skills": persona.must_have_skills,
            "nice_to_have_skills": persona.nice_to_have_skills,
            "experience_years": persona.experience_years,
            "motivations": persona.motivations,
            "preferred_channels": persona.preferred_channels,
            "keywords": persona.keywords,
        } if persona else None,
        "job_ad": {
            "headline": job_ad.headline,
            "body": job_ad.body,
            "call_to_action": job_ad.call_to_action,
        } if job_ad else None,
        "postings": [
            {"channel": p.channel, "status": p.status, "external_url": p.external_url}
            for p in campaign.postings
        ],
        "leads": [
            {
                "name": l.name,
                "source": l.source,
                "fit_score": l.fit_score,
                "status": l.status,
                "last_message": l.last_message,
            }
            for l in campaign.leads
        ],
        "analytics": {
            "impressions": analytics.impressions,
            "clicks": analytics.clicks,
            "applications": analytics.applications,
            "qualified_leads": analytics.qualified_leads,
            "interviews": analytics.interviews,
            "hires": analytics.hires,
            "click_through_rate": analytics.click_through_rate,
            "application_rate": analytics.application_rate,
        } if analytics else None,
    }


@app.get("/")
def root():
    return {"message": "AI-Powered Recruitment Marketing Platform API is running."}
