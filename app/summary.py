import openai
from .config import Config

def summarize_abstracts(abstracts, max_papers=5):
    """Summarize a list of abstracts using OpenAI's API."""
    if not abstracts:
        return []
    
    # Debug: Check if API key is configured
    if not Config.OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is not set in environment variables")
        return "Error: OpenAI API key is not configured. Please set OPENAI_API_KEY in your environment variables."
    
    print(f"API Key configured: {'Yes' if Config.OPENAI_API_KEY else 'No'}")
    print(f"API Key length: {len(Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else 0}")
    print(f"API Key prefix: {Config.OPENAI_API_KEY[:7] if Config.OPENAI_API_KEY else 'None'}...")
        
    # Prepare the prompt
    prompt = (
        "You are a scientific paper summarizer. Your task is to analyze these recent Nature papers "
        "and provide concise, informative summaries.\n\n"
        "For each paper, write a single paragraph (2-3 sentences) that:\n"
        "1. States the key scientific question/problem\n"
        "2. Summarizes the main findings and their significance\n\n"
        "Format your response in HTML with the following structure:\n"
        "<div class='summary-section'>\n"
        "  <h2>Today's Highlights</h2>\n"
        "  <div class='paper-summaries'>\n"
        "    <div class='paper-summary'>\n"
        "      <h3>Paper 1 Title</h3>\n"
        "      <p>Summary text here...</p>\n"
        "    </div>\n"
        "    <!-- Repeat for each paper -->\n"
        "  </div>\n"
        "</div>\n\n"
        "Here are the abstracts:\n\n"
    )
    
    for i, abstract in enumerate(abstracts[:max_papers], 1):
        prompt += f"Abstract {i}:\n{abstract}\n\n"
    
    try:
        print("Initializing OpenAI client...")
        # Initialize OpenAI client with minimal configuration
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        print("OpenAI client initialized successfully")
        
        print("Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a scientific paper summarizer with expertise in analyzing research papers. Format your response in clean, semantic HTML."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        print("Received response from OpenAI API")
        
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        print(f"OpenAI API error: {str(e)}")
        return "Error: Unable to connect to OpenAI API. Please check your API key and try again."
    except Exception as e:
        print(f"Unexpected error in summarization: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {str(e)}")
        return "Error generating summaries. Please try again later."