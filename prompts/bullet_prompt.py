def build_bullet_prompt(bullet, jd_text):
    prompt = f"""You are an expert resume coach who specialises in writing powerful, 
achievement-focused resume bullets for software engineering roles.

ORIGINAL RESUME BULLET:
{bullet}

JOB DESCRIPTION (use keywords from this naturally):
{jd_text[:1500]}

INSTRUCTIONS:
- Rewrite the bullet using STAR format (Situation, Task, Action, Result)
- Naturally inject 2-3 relevant keywords from the job description
- Start with a strong action verb (Built, Designed, Implemented, Optimised, Led)
- Include a quantified result if possible (%, time saved, users impacted)
- Keep the rewritten bullet under 30 words
- Return ONLY valid JSON. No extra text. No markdown. No backticks.
- Your entire response must start with {{ and end with }}

Return exactly this JSON structure:
{{
    "original": "<the original bullet exactly as given>",
    "rewritten": "<the improved STAR format bullet>",
    "star_breakdown": {{
        "situation": "<what situation or context this was>",
        "task": "<what you were responsible for>",
        "action": "<what you specifically did>",
        "result": "<what the outcome or impact was>"
    }},
    "keywords_added": ["<keyword1>", "<keyword2>"]
}}"""

    return prompt