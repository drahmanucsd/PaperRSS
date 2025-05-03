import openai
from .models import Vote, Paper, db
from .config import Config

PREFS_FILE = "user_prefs_summary.txt"  # Or use DB if you prefer

def extract_user_preferences():
    # Get unused votes
    unused_votes = Vote.query.filter_by(used_for_prefs=False).all()
    if not unused_votes:
        return None  # Nothing new to update

    # Group by up/down
    upvoted_dois = [v.paper_doi for v in unused_votes if v.vote == 'up']
    downvoted_dois = [v.paper_doi for v in unused_votes if v.vote == 'down']

    upvoted_abstracts = [Paper.query.filter_by(doi=doi).first().abstract for doi in upvoted_dois]
    downvoted_abstracts = [Paper.query.filter_by(doi=doi).first().abstract for doi in downvoted_dois]

    # Load previous summary if exists
    try:
        with open(PREFS_FILE, "r") as f:
            prev_summary = f.read()
    except FileNotFoundError:
        prev_summary = ""

    # Prompt LLM
    prompt = (
        "You are an expert at analyzing user preferences for scientific articles.\n"
        "Here is the current summary of what users like and dislike:\n"
        f"{prev_summary}\n\n"
        "Here are new articles users upvoted:\n"
        + "\n".join(upvoted_abstracts) + "\n\n"
        "Here are new articles users downvoted:\n"
        + "\n".join(downvoted_abstracts) + "\n\n"
        "Update the summary of what users like and dislike in scientific articles. "
        "Be concise and specific. Format as:\n"
        "LIKES: ...\nDISLIKES: ...\n"
    )

    client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing user preferences for scientific articles."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )
    summary = response.choices[0].message.content.strip()

    # Save updated summary
    with open(PREFS_FILE, "w") as f:
        f.write(summary)

    # Mark votes as used
    for v in unused_votes:
        v.used_for_prefs = True
    db.session.commit()

    return summary

def get_user_preferences():
    try:
        with open(PREFS_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "" 