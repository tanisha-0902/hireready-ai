def build_predictor_prompt(resume_text, jd_text, experience_level):
    trimmed_resume = resume_text[:3000]

    prompt = f"""You are a senior technical interviewer with 15 years of experience 
hiring software engineers at top tech companies.

You are preparing to interview a candidate. Here is their resume and the job description.

CANDIDATE RESUME:
{trimmed_resume}

JOB DESCRIPTION:
{jd_text[:1500]}

CANDIDATE EXPERIENCE LEVEL: {experience_level}

Your task is to predict exactly 10 interview questions this specific candidate 
will likely be asked, based on THEIR resume and THIS job description.

Question mix required:
- 4 Technical questions (based on skills and projects in the resume vs JD requirements)
- 3 Behavioural questions (based on the candidate's background and experience)
- 2 Role-specific questions (based on the responsibilities in the JD)
- 1 Motivation or culture question

INSTRUCTIONS:
- Questions must be specific to THIS candidate, not generic
- For each question explain exactly why it will be asked based on the resume/JD
- Provide a clear step-by-step answer framework
- Write a sample strong answer tailored to this candidate's background
- Return ONLY valid JSON. No extra text. No markdown. No backticks.
- Your entire response must start with {{ and end with }}

Return exactly this JSON structure:
{{
    "role": "<detected role from the job description>",
    "questions": [
        {{
            "id": 1,
            "question": "<the actual interview question>",
            "category": "<exactly one of: Technical, Behavioural, Role-specific, Culture>",
            "why_asked": "<one sentence — why THIS question for THIS candidate>",
            "answer_framework": "<step by step guide on how to structure the answer>",
            "sample_strong_answer": "<example of a strong answer for this specific candidate>"
        }}
    ]
}}"""

    return prompt