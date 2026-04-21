import time
import pandas as pd
from core.pdf_parser import extract_text_from_pdf
from features.resume_analyzer import analyse_resume


def screen_resumes(uploaded_files, jd_text):
    # This list will collect one dictionary per resume
    # Think of it like a table — each dict is one row
    results = []

    # Loop through each uploaded file one by one
    # enumerate gives us both the index (i) and the file object
    for i, uploaded_file in enumerate(uploaded_files):
        print(f"Processing resume {i+1} of {len(uploaded_files)}: {uploaded_file.name}")

        try:
            # Step 1: Extract text from this PDF
            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text:
                # If extraction failed, add an error row and continue
                results.append({
                    "File Name": uploaded_file.name,
                    "Match Score": 0,
                    "Recommendation": "Error",
                    "Matched Skills": "Could not read PDF",
                    "Missing Skills": "",
                    "Overall Feedback": "PDF could not be parsed"
                })
                continue

            # Step 2: Call Driksha's analyse_resume function
            analysis = analyse_resume(resume_text, jd_text)

            if not analysis:
                # If AI analysis failed, add an error row and continue
                results.append({
                    "File Name": uploaded_file.name,
                    "Match Score": 0,
                    "Recommendation": "Error",
                    "Matched Skills": "AI analysis failed",
                    "Missing Skills": "",
                    "Overall Feedback": "Could not analyse this resume"
                })
                continue

            # Step 3: Pull the fields we want from the analysis dict
            # join() converts a list like ["Python","SQL"] to "Python, SQL"
            results.append({
                "File Name": uploaded_file.name,
                "Match Score": analysis.get("match_score", 0),
                "Recommendation": analysis.get("hiring_recommendation", "Unknown"),
                "Matched Skills": ", ".join(analysis.get("matched_skills", [])),
                "Missing Skills": ", ".join(analysis.get("missing_skills", [])),
                "Overall Feedback": analysis.get("overall_feedback", "")
            })

        except Exception as e:
            # If anything unexpected happens, log it and move to next file
            print(f"ERROR processing {uploaded_file.name}: {e}")
            results.append({
                "File Name": uploaded_file.name,
                "Match Score": 0,
                "Recommendation": "Error",
                "Matched Skills": "",
                "Missing Skills": "",
                "Overall Feedback": f"Unexpected error: {e}"
            })

        # Wait 1 second between API calls to avoid hitting rate limits
        # Like waiting between orders so the kitchen doesn't get overwhelmed
        if i < len(uploaded_files) - 1:
            time.sleep(1)

    # Convert the list of dicts into a pandas DataFrame (like an Excel table)
    df = pd.DataFrame(results)

    # Sort by Match Score — highest first
    df = df.sort_values(by="Match Score", ascending=False)

    # Reset the index so row numbers are clean after sorting
    df = df.reset_index(drop=True)

    return df