# HireReady AI — Job Readiness Platform

> Upload your resume. Paste a JD. Know exactly where you stand.

**[Live App]()** · Built with Python + Groq AI · Deployed on Streamlit Cloud

---

## What it does

| Feature | Description |
|---|---|
| Resume Analysis | Match score, skills gap, hiring recommendation |
| Bullet Rewriter | Rewrites weak bullets into STAR format |
| Interview Predictor | 10 tailored questions based on your resume + JD |
| Mock Interview | 8-round AI interview with scoring and report |
| Batch Screener | Screen multiple resumes, export as CSV |

---

## Run locally

```bash
git clone https://github.com/drikshathakur786/hireready-ai.git
cd hireready-ai
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
streamlit run app.py
```

Free API key at [console.groq.com](https://console.groq.com)

---

## Stack

Python · Streamlit · Groq LLaMA 3.3-70B · pdfplumber · pandas

---
