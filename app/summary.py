import openai
from .config import Config

def summarize_abstracts(abstracts, max_papers=5):
    """Summarize a list of abstracts using OpenAI's API."""
    if not abstracts:
        return []
        
    # Prepare the prompt
    prompt = (
        "Here are the abstracts from recent Nature papers. For each, write a 2-sentence summary "
        "focusing on novelty and key findings. Then list the top 3 most interesting works:\n\n"
    )
    
    for i, abstract in enumerate(abstracts[:max_papers], 1):
        prompt += f"Abstract {i}:\n{abstract}\n\n"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a scientific paper summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in summarization: {str(e)}")
        return "Error generating summaries. Please try again later." 