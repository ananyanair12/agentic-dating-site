<div align="center">

# 💘 Agentic Dating Site
### *Where AI Agents Date On Your Behalf*

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github)](https://github.com/ananyanair12/agentic-dating-site)

[🎥 Watch Demo Video (3 Min Max)](#-youtube-demo-video) • [🚀 Live Website](#-live-website) • [📊 View Compatibility Matrix](#-features)

---

### 📸 Application Preview

<p align="center">
  <img src="https://raw.githubusercontent.com/ananyanair12/agentic-dating-site/main/preview.png" alt="Agentic Dating Site Preview" width="100%" style="border-radius: 10px; border: 1px solid #334155;" />
</p>

> *A platform where real people are represented by AI agents that analyze their official LinkedIn & public Instagram profiles, converse on dates, and generate compatibility rankings.*

</div>

---

## 🌟 Features & Interactive Capabilities

- **🕵️ Real Profile Ingestion:** Ingests official public LinkedIn & public Instagram URLs for **25 real public figures/creators**.
- **🧠 Autonomous Persona Extraction:** Synthesizes hobbies, communication styles, values, and dating preferences into structured agent profiles.
- **💬 Live Agent Dating Simulation:** Watch AI agents chat in real time, evaluate mutual chemistry, and score dates dynamically.
- **🏆 Global Compatibility Matrix:** Calculates top mutual fit recommendations across all 25 candidate personas.
- **🔗 Custom URL Sandbox:** Paste custom LinkedIn and Instagram links to instantly analyze and date new candidates.

---

## ⚙️ Technical Architecture & Pipeline

<details>
<summary><b>🔍 Click to Expand System Flow Architecture</b></summary>

```text
 [ User Input: 25 Profiles (LinkedIn + Instagram URLs) ]
                        │
                        ▼
         ┌─────────────────────────────┐
         │ Scraping & Ingestion Engine │ (Apify / Proxycurl Integration)
         └──────────────┬──────────────┘
                        │ Raw Metadata
                        ▼
         ┌─────────────────────────────┐
         │ LLM Persona Generator       │ (Needs, Hobbies, Traits Extraction)
         └──────────────┬──────────────┘
                        │ Structured Agent Data
                        ▼
         ┌─────────────────────────────┐
         │ Multi-Agent Dating Harness  │ (Turn-based Chat Execution)
         └──────────────┬──────────────┘
                        │ Dialogue & Chemistry Logs
                        ▼
         ┌─────────────────────────────┐
         │ Compatibility Ranking Engine│ (Multi-candidate Match Scoring)
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │ Next.js / FastAPI Interface │ (Live Dating Demo & Matrix Dashboard)
         └─────────────────────────────┘