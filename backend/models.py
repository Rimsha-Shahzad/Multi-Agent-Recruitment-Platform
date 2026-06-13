from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    seniority = Column(String, default="Mid-level")
    status = Column(String, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)

    persona = relationship("Persona", back_populates="campaign", uselist=False, cascade="all, delete-orphan")
    job_ad = relationship("JobAd", back_populates="campaign", uselist=False, cascade="all, delete-orphan")
    postings = relationship("Posting", back_populates="campaign", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="campaign", cascade="all, delete-orphan")
    analytics = relationship("AnalyticsSnapshot", back_populates="campaign", uselist=False, cascade="all, delete-orphan")


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    title = Column(String)
    summary = Column(Text)
    must_have_skills = Column(JSON)
    nice_to_have_skills = Column(JSON)
    experience_years = Column(String)
    motivations = Column(JSON)
    preferred_channels = Column(JSON)
    keywords = Column(JSON)

    campaign = relationship("Campaign", back_populates="persona")


class JobAd(Base):
    __tablename__ = "job_ads"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    headline = Column(String)
    body = Column(Text)
    call_to_action = Column(String)

    campaign = relationship("Campaign", back_populates="job_ad")


class Posting(Base):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    channel = Column(String)  # LinkedIn, Indeed, Google Jobs, Company Site
    status = Column(String)   # posted, failed
    external_url = Column(String)
    posted_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="postings")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    name = Column(String)
    source = Column(String)
    fit_score = Column(Float)
    status = Column(String, default="New")  # New, Nurturing, Engaged, Interview, Hired
    last_message = Column(Text)

    campaign = relationship("Campaign", back_populates="leads")


class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    applications = Column(Integer, default=0)
    qualified_leads = Column(Integer, default=0)
    interviews = Column(Integer, default=0)
    hires = Column(Integer, default=0)
    click_through_rate = Column(Float, default=0.0)
    application_rate = Column(Float, default=0.0)
    generated_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="analytics")
