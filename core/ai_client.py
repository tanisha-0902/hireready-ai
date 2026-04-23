import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Load key from Streamlit Cloud secrets OR local .env
# This makes the app work both locally and when deployed
try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("WARNING: GROQ_API_KEY is not set.")
    client = None
else:
    # Groq() creates the client — same waiter analogy as before,
    # just a different restaurant (Groq instead of Google).
    client = Groq(api_key=api_key)


def call_claude(prompt, max_tokens=1024):
    # Still named call_claude so every other file works without changes.
    if client is None:
        print("ERROR: Groq client is not set up. Check your .env file.")
        return None

    try:
        # Groq uses the same message format as OpenAI.
        # model: llama-3.3-70b-versatile is free, fast, and very capable.
        # It's actually better than gemini-flash for structured JSON tasks.
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # response.choices[0].message.content gives us the text reply.
        return response.choices[0].message.content

    except Exception as e:
        print(f"ERROR: Something went wrong calling Groq: {e}")
        return None


if __name__ == "__main__":
    print("Testing Groq connection...")
    response = call_claude("Say hello and tell me today's date. Reply in one sentence.")

    if response:
        print("SUCCESS! Groq says:")
        print(response)
    else:
        print("FAILED — check the error message above.")