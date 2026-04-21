import json
from core.ai_client import call_claude
from prompts.analyzer_prompt import build_analyzer_prompt

# These are the keys we expect in every valid AI response.
# If any of these are missing, something went wrong.
REQUIRED_KEYS = [
    "match_score",
    "hiring_recommendation",
    "recommendation_reason",
    "matched_skills",
    "missing_skills",
    "experience_match",
    "education_match",
    "overall_feedback"
]


def clean_json_response(raw_response):
    # Sometimes the AI adds backticks or the word "json" before the JSON.
    # Example of what we might get: ```json { ... } ```
    # This function strips all that out so json.loads() can read it cleanly.

    # Remove markdown code fences like ```json and ```
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        # Find the first { and last } and extract just that part
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end != 0:
            cleaned = cleaned[start:end]

    return cleaned


def analyse_resume(resume_text, jd_text):
    # Step 1: Build the prompt using our prompt builder function
    prompt = build_analyzer_prompt(resume_text, jd_text)

    # Step 2: Send the prompt to the AI and get raw text back
    # We use max_tokens=1500 because the response has many fields
    raw_response = call_claude(prompt, max_tokens=1500)

    # If the API call failed, raw_response will be None
    if raw_response is None:
        print("ERROR: AI call failed in analyse_resume")
        return None

    # Step 3: Clean the response in case the AI added extra formatting
    cleaned_response = clean_json_response(raw_response)

    # Step 4: Parse the JSON string into a Python dictionary.
    # A dictionary is like a contact book — each entry has a name (key)
    # and a value. Example: {"match_score": 72, "matched_skills": ["Python"]}
    try:
        result = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse AI response as JSON: {e}")
        print(f"Raw response was: {raw_response[:200]}")
        return None

    # Step 5: Validate that all required keys exist in the response
    for key in REQUIRED_KEYS:
        if key not in result:
            print(f"ERROR: Missing key in AI response: {key}")
            return None

    # Step 6: Make sure match_score is actually a number between 0-100
    try:
        result["match_score"] = int(result["match_score"])
        if not 0 <= result["match_score"] <= 100:
            result["match_score"] = max(0, min(100, result["match_score"]))
    except (ValueError, TypeError):
        print("ERROR: match_score is not a valid number")
        return None

    return result


if __name__ == "__main__":
    # Test with a fake resume and fake JD
    fake_resume = """
    Priya Mehta
    CS Student, Pune University | CGPA: 8.2
    
    Skills: Python, React, Node.js, SQL, Git, MongoDB
    
    Projects:
    - Built a To-Do web app using React and Node.js with user authentication
    - Created a data analysis script in Python using pandas to analyse sales data
    
    Internship:
    - Frontend Intern at TechStartup (2 months)
    - Built 3 React components used in production
    """

    fake_jd = """
    Full Stack Developer — 0-2 years experience
    Required: React, Node.js, PostgreSQL, REST APIs, Git
    Nice to have: Docker, AWS
    """

    print("Testing resume analyser...")
    print("Sending to AI — this may take 5-10 seconds...\n")

    result = analyse_resume(fake_resume, fake_jd)

    if result:
        print("SUCCESS! Here is the analysis:")
        print(json.dumps(result, indent=2))
    else:
        print("FAILED — check error messages above")