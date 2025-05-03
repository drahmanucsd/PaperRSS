import openai
from .config import Config

def select_highlighted_paper(papers, user_prefs):
    # papers: list of Paper objects
    prompt = (
        "Users like articles with these properties:\n"
        f"{user_prefs}\n\n"
        "Here are today's articles:\n"
    )
    for i, paper in enumerate(papers, 1):
        prompt += f"Paper {i}:\nTitle: {paper.title}\nAbstract: {paper.abstract}\n\n"

    prompt += (
        "Pick the one article from the list above that users are most likely to upvote, "
        "based on their preferences. Return the title of the highlighted article and a short justification. "
        "Format as:\nTITLE: ...\nJUSTIFICATION: ...\n"
    )

    client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert at matching articles to user preferences."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )
    result = response.choices[0].message.content.strip()
    # Parse result
    title = ""
    justification = ""
    for line in result.splitlines():
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("JUSTIFICATION:"):
            justification = line.replace("JUSTIFICATION:", "").strip()
    return title, justification 