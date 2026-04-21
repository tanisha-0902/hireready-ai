import json
import re
from core.ai_client import call_claude
from prompts.bullet_prompt import build_bullet_prompt


REQUIRED_KEYS = ["original", "rewritten", "star_breakdown", "keywords_added"]


def clean_json_response(raw_response):
    # Same cleaner as resume_analyzer — strips backticks if AI adds them
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end != 0:
            cleaned = cleaned[start:end]
    return cleaned


def rewrite_bullet(bullet, jd_text):
    # Step 1: Build the prompt
    prompt = build_bullet_prompt(bullet, jd_text)

    # Step 2: Call the AI
    raw_response = call_claude(prompt, max_tokens=1000)

    if raw_response is None:
        print("ERROR: AI call failed in rewrite_bullet")
        return None

    # Step 3: Clean and parse JSON
    cleaned = clean_json_response(raw_response)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON in rewrite_bullet: {e}")
        print(f"Raw response: {raw_response[:200]}")
        return None

    # Step 4: Validate required keys exist
    for key in REQUIRED_KEYS:
        if key not in result:
            print(f"ERROR: Missing key in bullet rewrite response: {key}")
            return None

    return result


def extract_bullets(resume_text):
    # A Python list is like a shopping list — an ordered collection of items.
    # We'll collect all bullet points we find and return them as a list.
    bullets = []

    # Split the resume into individual lines
    # splitlines() is like tearing a page into individual strips of paper
    lines = resume_text.splitlines()

    for line in lines:
        # Remove leading and trailing whitespace from each line
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Check if line starts with a bullet symbol
        is_bullet_symbol = stripped.startswith(("•", "-", "*", "–", "▪"))

        # Check if line looks like an accomplishment:
        # — longer than 20 characters (not just a heading)
        # — shorter than 200 characters (not a paragraph)
        # — contains a verb-like word suggesting action
        action_words = [
            "built", "developed", "created", "designed", "implemented",
            "led", "managed", "optimised", "optimized", "improved",
            "reduced", "increased", "achieved", "delivered", "launched",
            "worked", "collaborated", "wrote", "tested", "deployed",
            "automated", "integrated", "maintained", "analysed", "analyzed"
        ]
        has_action_word = any(
            word in stripped.lower() for word in action_words
        )
        is_accomplishment = (
            20 < len(stripped) < 200 and has_action_word
        )

        if is_bullet_symbol or is_accomplishment:
            # Clean the bullet symbol off the front if present
            clean_bullet = re.sub(r'^[•\-\*–▪]\s*', '', stripped)
            if clean_bullet and clean_bullet not in bullets:
                bullets.append(clean_bullet)

    # COMMON MISTAKE: if bullets list is empty, warn clearly
    if not bullets:
        print("WARNING: No bullets found in resume text.")
        print("This usually means the PDF text extraction lost formatting.")
        print("Returning full lines as fallback.")
        # Fallback — return any line between 20-150 chars as a potential bullet
        for line in lines:
            stripped = line.strip()
            if 20 < len(stripped) < 150 and stripped not in bullets:
                bullets.append(stripped)

    return bullets


if __name__ == "__main__":
    fake_bullet = "Worked on authentication feature for the web app"

    fake_jd = """
    Full Stack Developer — 0-2 years
    Required: React, Node.js, PostgreSQL, REST APIs, Git
    Nice to have: Docker, AWS, JWT, security
    """

    print("Testing bullet rewriter...")
    print("Sending to AI — this may take 5-10 seconds...\n")

    result = rewrite_bullet(fake_bullet, fake_jd)

    if result:
        print("SUCCESS! Here is the rewrite:")
        print(json.dumps(result, indent=2))
    else:
        print("FAILED — check error messages above")

    print("\n--- Testing extract_bullets ---")
    fake_resume = """
    Priya Mehta — Software Developer
    
    Experience:
    • Built a To-Do app using React and Node.js with user authentication
    • Developed data analysis script in Python reducing report time by 60%
    - Collaborated with 3 designers to implement pixel-perfect UI components
    * Deployed application to AWS EC2 serving 200+ daily users
    
    Education:
    BE Computer Science, Pune University, CGPA 8.2
    """

    bullets = extract_bullets(fake_resume)
    print(f"\nFound {len(bullets)} bullets:")
    for i, b in enumerate(bullets, 1):
        print(f"  {i}. {b}")