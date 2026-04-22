import json
from core.ai_client import call_claude
from prompts.predictor_prompt import build_predictor_prompt


def clean_json_response(raw_response):
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end != 0:
            cleaned = cleaned[start:end]
    return cleaned


def predict_questions(resume_text, jd_text, experience_level="Fresher"):
    # Step 1: Build the prompt
    prompt = build_predictor_prompt(resume_text, jd_text, experience_level)

    # Step 2: Call AI with more tokens — 10 detailed questions needs more space
    # Think of max_tokens like the maximum number of words the AI can write back
    raw_response = call_claude(prompt, max_tokens=3000)

    if raw_response is None:
        print("ERROR: AI call failed in predict_questions")
        return None

    # Step 3: Clean and parse
    cleaned = clean_json_response(raw_response)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON in predict_questions: {e}")
        print(f"Raw response was: {raw_response[:300]}")
        return None

    # Step 4: Validate the top level keys exist
    if "questions" not in result:
        print("ERROR: 'questions' key missing from AI response")
        return None

    if "role" not in result:
        print("WARNING: 'role' key missing, setting default")
        result["role"] = "Software Developer"

    # Step 5: Validate we got enough questions
    questions = result["questions"]
    if len(questions) < 5:
        print(f"WARNING: Only got {len(questions)} questions, expected 10")
        print("This can happen with strict rate limits — try again")
        # We still return what we got rather than returning None
        # Partial results are better than no results

    # Step 6: Validate each question has required fields
    required_question_keys = [
        "id", "question", "category", "why_asked",
        "answer_framework", "sample_strong_answer"
    ]

    valid_questions = []
    for q in questions:
        # Only keep questions that have all required fields
        if all(key in q for key in required_question_keys):
            valid_questions.append(q)
        else:
            print(f"WARNING: Skipping malformed question: {q.get('id', '?')}")

    result["questions"] = valid_questions
    return result


if __name__ == "__main__":
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

    print("Testing interview question predictor...")
    print("Sending to AI — this may take 10-15 seconds...\n")

    result = predict_questions(fake_resume, fake_jd, "Fresher")

    if result:
        print(f"SUCCESS! Role detected: {result['role']}")
        print(f"Total questions generated: {len(result['questions'])}\n")
        for q in result["questions"]:
            print(f"Q{q['id']} [{q['category']}]: {q['question']}")
            print(f"   Why asked: {q['why_asked']}")
            print()
    else:
        print("FAILED — check error messages above")