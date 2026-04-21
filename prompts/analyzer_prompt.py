def build_analyzer_prompt(resume_text, jd_text):
    # We trim the resume to 3000 characters to keep the prompt short.
    # Most important resume info is in the first 3000 characters anyway.
    # Sending too much text slows the API down and costs more tokens.
    trimmed_resume = resume_text[:3000]

    # This is the full prompt string we send to the AI.
    # We use an f-string so we can insert the actual resume and JD text.
    # Triple quotes """ let us write a multi-line string cleanly.
    prompt = f"""You are an expert career coach and technical recruiter with 10 years of experience in the tech industry.

Your task is to analyse a candidate's resume against a job description and return a detailed assessment.

RESUME:
{trimmed_resume}

JOB DESCRIPTION:
{jd_text}

INSTRUCTIONS:
- Compare the resume carefully against the job description
- Identify skills that match and skills that are missing
- Be realistic with the match score — most candidates score between 40-80%
- Return ONLY valid JSON. No extra text. No markdown. No backticks. No explanations.
- Your entire response must start with {{ and end with }}

Return exactly this JSON structure:
{{
    "match_score": <number between 0 and 100>,
    "hiring_recommendation": "<exactly one of: Strong Yes, Yes, Maybe, No>",
    "recommendation_reason": "<one sentence explaining the recommendation>",
    "matched_skills": ["<skill1>", "<skill2>"],
    "missing_skills": ["<skill1>", "<skill2>"],
    "experience_match": "<exactly one of: Strong, Good, Weak>",
    "education_match": "<exactly one of: Strong, Good, Weak>",
    "overall_feedback": "<2-3 sentences of honest, helpful feedback for the candidate>"
}}"""

    return prompt