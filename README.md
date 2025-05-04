# PaperRSS

PaperRSS is a Flask-based web application that creates daily digests of scientific papers from Nature journals. It fetches articles via RSS feeds, generates summaries using OpenAI, and publishes them as HTML pages.

## Features

- Daily fetching of articles from Nature journals via RSS
- Automatic generation of 2-sentence summaries using OpenAI
- Paper ranking based on user preferences
- HTML digest generation with clean, readable formatting
- GitHub Pages integration for publishing digests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PaperRSS.git
cd PaperRSS
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
```

## Usage

1. Configure your preferences in `preferences.txt` with your research interests.

2. Run the application:
```bash
python run.py
```

The script will:
- Fetch today's articles from configured Nature journals
- Generate summaries using OpenAI
- Rank articles based on your preferences
- Generate an HTML digest
- Publish to GitHub Pages

## Project Structure

```
PaperRSS/
├── app/                    # Application package
│   ├── __init__.py        # Flask app initialization
│   ├── config.py          # Configuration settings
│   ├── fetcher.py         # RSS feed fetching
│   ├── summarizer.py      # OpenAI summarization
│   ├── ranker.py          # Article ranking
│   ├── renderer.py        # HTML generation
│   └── github_uploader.py # GitHub Pages integration
├── digests/               # Generated digest files
├── tests/                 # Test suite
├── preferences.txt        # User preferences
├── requirements.txt       # Project dependencies
└── run.py                # Main execution script
```

## Development

Run tests:
```bash
pytest
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
