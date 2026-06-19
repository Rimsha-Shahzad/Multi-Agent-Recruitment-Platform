"use client";

import { useState } from "react";
import "./globals.css";

// 🔗 DYNAMIC GATEWAY: Automatically switches between local testing and your active live tunnel
const API_URL = typeof window !== 'undefined' && window.location.hostname === 'localhost'
  ? 'http://localhost:8005'
  : 'https://poor-flies-drop.loca.lt';;

const STAGES = [
  { key: "persona", name: "Persona Agent", desc: "Profiles the ideal candidate for this role." },
  { key: "job_ad", name: "Content Agent", desc: "Writes the job ad headline and copy." },
  { key: "postings", name: "Distribution Agent", desc: "Posts the ad across job channels." },
  { key: "leads", name: "Engagement Agent", desc: "Sources and nurtures candidate leads." },
  { key: "analytics", name: "Analytics Agent", desc: "Tracks pipeline performance metrics." },
];

export default function Home() {
  const [form, setForm] = useState({
    job_title: "Senior Software Engineer",
    company: "Acme Corp",
    location: "Lahore, Pakistan",
    seniority: "Senior",
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true); 
    setError(null);
    setResult(null);
    try {
      // 🎯 TARGETED DIRECT ABSOLUTE ROUTE WITH DYNAMIC BASE URL
      const res = await fetch(`${API_URL}/api/campaigns/run`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          // 🛡️ SECURITY BYPASS FOR BOTH INTERSTITIAL TUNNEL ENGINES
          "ngrok-skip-browser-warning": "true",
          "Bypass-Tunnel-Reminder": "true" 
        },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error(`Server responded with code: ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(
        `Could not reach backend at ${API_URL} (${err.message}). Ensure your Python backend terminal is running on port 8005.`
      );
    } finally {
      setLoading(false);
    }
  }

  function getRealUrl(channel, jobTitle, location) {
    const cleanTitle = encodeURIComponent(jobTitle);
    const cleanLocation = encodeURIComponent(location);
    const fullQuery = encodeURIComponent(`${jobTitle} ${location}`);

    if (channel.toLowerCase() === "linkedin") {
      return `https://www.linkedin.com/jobs/search/?keywords=${cleanTitle}&location=${cleanLocation}`;
    }
    if (channel.toLowerCase() === "indeed") {
      return `https://pk.indeed.com/jobs?q=${cleanTitle}&l=${cleanLocation}`;
    }
    if (channel.toLowerCase() === "google jobs") {
      return `https://www.google.com/search?q=${fullQuery}+jobs`;
    }
    return `https://www.google.com/search?q=${encodeURIComponent(form.company)}+careers`;
  }

  return (
    <main className="page">
      <p className="eyebrow">AI-Powered Recruitment Marketing Platform</p>
      <h1 className="title">Agent Pipeline Dashboard V3 FORCE CLEAN</h1>
      <p className="subtitle">
        Enter a role below and run it through the five-agent LangGraph pipeline:
        persona profiling, ad generation, multi-channel distribution, lead
        engagement, and analytics — end to end.
      </p>

      <form className="form-card" onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="field">
            <label htmlFor="job_title">Job title</label>
            <input id="job_title" name="job_title" value={form.job_title} onChange={handleChange} required />
          </div>
          <div className="field">
            <label htmlFor="company">Company</label>
            <input id="company" name="company" value={form.company} onChange={handleChange} required />
          </div>
          <div className="field">
            <label htmlFor="location">Location</label>
            <input id="location" name="location" value={form.location} onChange={handleChange} required />
          </div>
          <div className="field">
            <label htmlFor="seniority">Seniority</label>
            <select id="seniority" name="seniority" value={form.seniority} onChange={handleChange}>
              <option>Junior</option>
              <option>Mid-level</option>
              <option>Senior</option>
              <option>Lead</option>
            </select>
          </div>
        </div>
        <button className="run-button" type="submit" disabled={loading}>
          {loading ? "Running pipeline..." : "Run campaign"}
        </button>
        {error && <div className="error-banner">{error}</div>}
      </form>

      <div className="pipeline">
        {STAGES.map((stage, i) => (
          <div
            key={stage.key}
            className={`stage ${loading ? "active" : result ? "done" : ""}`}
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <div className="stage-status" />
            <div className="stage-number">{String(i + 1).padStart(2, "0")}</div>
            <div className="stage-name">{stage.name}</div>
            <div className="stage-desc">{stage.desc}</div>
          </div>
        ))}
      </div>

      {result && (
        <>
          <section>
            <p className="section-title">Persona Agent · Ideal Candidate</p>
            <div className="card">
              <h3>{result.persona.title}</h3>
              <p style={{ color: "var(--muted)", lineHeight: 1.7 }}>{result.persona.summary}</p>
              <div className="tag-row">
                {result.persona.must_have_skills?.map((s) => (
                  <span key={s} className="tag accent">{s}</span>
                ))}
                {result.persona.nice_to_have_skills?.map((s) => (
                  <span key={s} className="tag">{s}</span>
                ))}
              </div>
              <div className="tag-row">
                {result.persona.keywords?.map((k) => (
                  <span key={k} className="tag">#{k}</span>
                ))}
              </div>
            </div>
          </section>

          <section>
            <p className="section-title">Content Agent · Generated Job Ad</p>
            <div className="card">
              <h3>{result.job_ad.headline}</h3>
              <div className="job-ad-body">{result.job_ad.body}</div>
              <div style={{ display: "flex", justifyContent: "center", marginTop: "1rem" }}>
                <a 
                  href={getRealUrl("linkedin", form.job_title, form.location)} 
                  target="_blank" 
                  rel="noreferrer" 
                  className="cta" 
                  style={{ textDecoration: "none", display: "inline-block", cursor: "pointer", textAlign: "center" }}
                >
                  {result.job_ad.call_to_action}
                </a>
              </div>
            </div>
          </section>

          <section>
            <p className="section-title">Distribution Agent · Channels</p>
            <div className="card">
              <div className="channel-grid">
                {result.postings.map((p) => (
                  <div className="channel-card" key={p.channel}>
                    <div className="channel-name">{p.channel}</div>
                    <div className="channel-status">{p.status}</div>
                    <a 
                      className="channel-url" 
                      href={getRealUrl(p.channel, form.job_title, form.location)} 
                      target="_blank" 
                      rel="noreferrer"
                    >
                      Open Live Portal Listing ↗
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section>
            <p className="section-title">Engagement Agent · Candidate Leads</p>
            <div className="card">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Source</th>
                    <th>Fit score</th>
                    <th>Status</th>
                    <th>Last message</th>
                  </tr>
                </thead>
                <tbody>
                  {result.leads.map((l) => (
                    <tr key={l.name}>
                      <td>{l.name}</td>
                      <td>{l.source}</td>
                      <td>{l.fit_score}</td>
                      <td>
                        <span className={`status-pill status-${l.status}`}>{l.status}</span>
                      </td>
                      <td style={{ color: "var(--muted)" }}>{l.last_message}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section>
            <p className="section-title">Analytics Agent · Pipeline Metrics</p>
            <div className="card">
              <div className="metrics-grid">
                <div className="metric">
                  <div className="metric-value">{result.analytics.impressions.toLocaleString()}</div>
                  <div className="metric-label">Impressions</div>
                </div>
                <div className="metric">
                  <div className="metric-value">{result.analytics.clicks.toLocaleString()}</div>
                  <div className="metric-label">Clicks</div>
                </div>
                <div className="metric">
                  <div className="metric-value">{result.analytics.applications}</div>
                  <div className="metric-label">Applications</div>
                </div>
                <div className="metric">
                  <div className="metric-value">{result.analytics.qualified_leads}</div>
                  <div className="metric-label">Qualified leads</div>
                </div>
                <div className="metric">
                  <div className="metric-value">{result.analytics.interviews}</div>
                  <div className="metric-label">Interviews</div>
                </div>
                <div className="metric">
                  <div className="metric-value">{result.analytics.click_through_rate}%</div>
                  <div className="metric-label">Click-through rate</div>
                </div>
                <div className="metric">
                  <div className="metric-value">{result.analytics.application_rate}%</div>
                  <div className="metric-label">Application rate</div>
                </div>
                <div className="metric">
                  <div className="metric-value">{result.analytics.hires}</div>
                  <div className="metric-label">Hires</div>
                </div>
              </div>
            </div>
          </section>

          <section>
            <p className="section-title">Agent Execution Log</p>
            <div className="card">
              <ul className="log-list">
                {result.log.map((entry, i) => (
                  <li key={i}>{entry}</li>
                ))}
              </ul>
            </div>
          </section>
        </>
      )}
    </main>
  );
}