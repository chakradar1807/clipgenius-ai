from openai import OpenAI
client = OpenAI()

def get_transcript_summary(transcript):
    prompt = f"""
    Analyze this podcast transcript and extract:
    1. Top 5 most important moments
    2. Each moment with start time, end time (approx)
    3. Give a hook caption

    Transcript:
    {transcript[:8000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content