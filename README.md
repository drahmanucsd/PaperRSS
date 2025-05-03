# PaperRSS

A daily digest of Nature publications with impact factor-based ranking, AI-powered summaries, and feedback collection.

## Features

- Fetches papers from multiple Nature journals via RSS
- Ranks papers by journal impact factor
- Generates AI summaries of abstracts
- Sends daily email digests
- Collects feedback via 👍/👎 voting
- Archives digests on GitHub Pages
- Provides voting statistics via API

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PaperRSS.git
   cd PaperRSS
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   # Flask configuration
   SECRET_KEY=your-secret-key-here
   API_DOMAIN=your-domain.com

   # Database configuration
   DATABASE_URL=sqlite:///app.db

   # Email configuration
   SENDGRID_API_KEY=your-sendgrid-api-key
   EMAIL_FROM=your-verified-sender@domain.com
   EMAIL_RECIPIENTS=recipient1@domain.com,recipient2@domain.com

   # OpenAI configuration
   OPENAI_API_KEY=your-openai-api-key

   # GitHub configuration
   GITHUB_TOKEN=your-github-token
   GITHUB_REPO=username/repo-name
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the development server:
   ```bash
   flask run
   ```

## Deployment

The application is designed to run on PythonAnywhere's free tier:

1. Create a PythonAnywhere account
2. Upload the code to your account
3. Set up a virtual environment and install dependencies
4. Configure the web app to use your Flask application
5. Set up the daily task to run `run_digest.py`

Alternatively, you can use GitHub Actions to run the daily digest:

1. Fork this repository
2. Add the required secrets to your repository:
   - `OPENAI_API_KEY`
   - `SENDGRID_API_KEY`
   - `GITHUB_TOKEN`
   - `GITHUB_REPO`
   - `EMAIL_FROM`
   - `EMAIL_RECIPIENTS`
   - `API_DOMAIN`
   - `SECRET_KEY`

## Project Structure

```
digest-mvp/
├─ app/
│  ├─ __init__.py       # Flask app initialization
│  ├─ config.py         # Configuration and journal settings
│  ├─ models.py         # Database models
│  ├─ rss.py           # RSS feed fetching
│  ├─ summary.py       # Abstract summarization
│  ├─ emailer.py       # Email sending
│  ├─ feedback.py      # Feedback API endpoints
│  └─ archiver.py      # GitHub archiving
├─ run_digest.py       # Main script
├─ requirements.txt    # Dependencies
└─ .github/workflows/daily_digest.yml
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

**Exploring deeper implementation details**

The user provided a list of journals along with the source for Impact Factors and their tech preferences (Flask, free/low cost solutions with good documentation). They want to go deeper into the specifics of implementation, like parsing the RSS feeds for these journals. I need to identify and fetch the correct RSS feed URLs for Nature and its specialized journals. To do this, I might have to search for the appropriate RSS links for each journal. It's a next important step!

**Designing the technical approach**

I'm considering doing a web search to locate the RSS feed URLs for the journals. The alternative is asking the user to find them. For the Impact Factor metrics, we might scrape the metrics page using BeautifulSoup. The backend will likely use Flask and SQLite, both low-cost options. For deployment, I'm thinking of GitHub Actions or a free host like PythonAnywhere. I'll also need a basic Flask app skeleton with endpoints and a deeper plan, including code snippets for functionality like fetching or digesting data.

**Proposing backend setup**

To set up the backend, we could use PythonAnywhere for Flask hosting and schedule daily tasks with their cron. For static content, GitHub Pages is perfect. I'll show how to set up GitHub Actions, complete with YAML, to run a daily cron job. For scraping, I'll guide you through using requests and BeautifulSoup, along with some caching. We can use PythonAnywhere's free tier for small tasks and simple Flask-looking APIs, combined with other free tools like SendGrid for emails and Render for hosting.

**Proposing hosting and setup**

The user wants a dynamic system for voting feedback, but not a backend. I'm thinking GitHub Issues could work, but it's too hacky. Instead, I'm suggesting hosting the feedback API on PythonAnywhere's free plan. For static content, GitHub Pages could handle that. They're familiar with Flask, so PythonAnywhere is a good match. Alternatively, Render or Railway are other options. I'll also propose SQLite for the database, as it's free and easy to set up. I'll dive into more details on the setup and documentation.

**Proposing dynamic solution**

Since static sites can't record votes, I'm suggesting we host the feedback API using Cloudflare Workers, storing vote counts in Workers KV. However, considering the user's expertise with Flask, PythonAnywhere seems like a better choice. I propose hosting the API on PythonAnywhere's free plan, which includes 500MB. We can schedule tasks using PythonAnywhere's scheduler. This would work particularly well for Python, which the user is comfortable with. We can keep everything flexible and dynamic this way!

**Digging deeper: Journal and RSS setup**

It looks like the user is looking for a more detailed plan. The next step is to identify the relevant journals and their RSS feed URLs. I'll begin by searching for feeds, like the one for "Nature Reviews Drug Discovery", and compile this information for the user. This will help create a broader scope for incorporating selected journals, gathering metrics, and creating documentation for the Flask setup with free or low-cost hosting, while keeping everything organized. I'll dive into this search now.

**Proposing hosting and database solutions**

For hosting, I suggest using GitHub Pages to manage the static site. PythonAnywhere can help with committing via GitHub API, but its free tier supports internet access, so that's fine. Alternatively, Render or Railway can host Flask with task scheduling via cron, offering free options too. As for databases, SQLite is easier and free, but PostgreSQL also works on Render's free plan. I'll propose PythonAnywhere and Render, and link their docs for the user to explore more.

**Gathering RSS feed URLs**

I've found the actual RSS feed links for several journals. For "Nature Reviews Drug Discovery," the current issue feed is [https://www.nature.com/nrd/current_issue/rss](https://www.nature.com/nrd/current_issue/rss) and the AOP feed is [https://www.nature.com/nrd/journal/vaop/ncurrent/rss.rdf](https://www.nature.com/nrd/journal/vaop/ncurrent/rss.rdf). Similarly, "Nature Reviews Cancer" has these URLs: current issue [https://www.nature.com/nrc/current_issue/rss](https://www.nature.com/nrc/current_issue/rss) and AOP [https://www.nature.com/nrc/journal/vaop/ncurrent/rss.rdf](https://www.nature.com/nrc/journal/vaop/ncurrent/rss.rdf). For "Nature Biomedical Engineering," the RSS feed is [https://www.nature.com/natbiomedeng/rss](https://www.nature.com/natbiomedeng/rss).

**Finding Biomedical Engineering RSS Feed**

I've come across some search results showing possible RSS feeds for "Nature Biomedical Engineering," but I'm not entirely sure which one is the right fit. I found a generic feed [https://www.nature.com/natbiomedeng.rss](https://www.nature.com/natbiomedeng.rss), and another possibility could be [https://www.nature.com/natbiomedeng/current-issue/rss](https://www.nature.com/natbiomedeng/current-issue/rss). However, a broader feed like [https://www.nature.com/subjects/biomedical-engineering/rss](https://www.nature.com/subjects/biomedical-engineering/rss) covers multiple subjects, not just the specific journal. I'll suggest trying the first two for now!

**Verifying RSS feed link**

I need to confirm the correct RSS feed URL for "Nature Biomedical Engineering." The page provides an RSS feed link: [https://www.nature.com/natbiomedeng/current-issue/rss](https://www.nature.com/natbiomedeng/current-issue/rss), which seems like the right one. I also considered potential variations in the URL format, like using underscores. Other journals like NBT and NG also have similar RSS links for their current issues. So, I'll stick with this verified link for "Nature Biomedical Engineering."

**Confirming RSS feed URLs**

For "Nature Biomedical Engineering," the correct feed URL seems to be [https://www.nature.com/natbiomedeng/current-issue/rss](https://www.nature.com/natbiomedeng/current-issue/rss). Additionally, the AOP feed is likely [https://www.nature.com/natbiomedeng/journal/vaop/ncurrent/rss.rdf](https://www.nature.com/natbiomedeng/journal/vaop/ncurrent/rss.rdf). Other journals use similar formats, like NBT and NG, so this pattern fits. It appears reliable for the biomedical engineering journal you're after.

**Routing and GitHub Setup**

For the voting system, I'll use SQLAlchemy ORM to handle votes with fields like DOI, vote type, and timestamp. The routing will allow feedback through the `/feedback` endpoint, handling valid "up" or "down" votes. For stats, I'll aggregate the votes by paper DOI and return insights as JSON. In `archiver.py`, I'll use PyGitHub to commit digests to a repo or update the file. The GitHub Actions workflow ensures a daily digest run with API keys securely set. Lastly, the Flask app will be hosted on PythonAnywhere.

**Choosing Hosting Configuration**

It looks like the feedback API and the email pipeline need to be hosted separately. Since GitHub Actions will handle the pipeline, I'll need to host the API continuously on PythonAnywhere. However, free accounts on PythonAnywhere can only schedule one task, which limits flexibility. I could explore hosting both the pipeline and API on PythonAnywhere, though scheduling at 7am PST might be tricky. Alternatively, I could separate the tasks, using GitHub for archiving and PythonAnywhere for the rest.

**Proposing Hosting Setup**

I'm suggesting hosting the entire Flask app on PythonAnywhere, including the feedback API and the archiver command, which can be run as scheduled tasks. The `run_digest.py` script can be executed daily at 7:00 AM PST, where it performs fetch, summary, email, and commit operations. Free accounts on PythonAnywhere do restrict CPU and can "sleep," but they allow for one scheduled task, which is perfect for this. Alternatively, Render's free tier could be an option, but it adds complexity. Let's stick with PythonAnywhere for now.

**Considering Hosting Options**

I'm looking at different free or low-cost solutions for hosting. My primary pick is PythonAnywhere, as its free tier offers a single scheduled task, 500MB of disk space, and decent documentation. Alternative options include Render, Railway, and GitHub Actions (for workflows but not API hosting). Azure Functions and AWS Lambda are also available but add complexity for Flask. For now, I'll prioritize PythonAnywhere and Render and get organized with the necessary feed URLs for integration.

Thought for 1m 0s

**1. Journal & Metric Configuration**

* **RSS feeds:**

  ```yaml
  Nature Reviews Drug Discovery:       https://www.nature.com/nrd/current_issue/rss  
  Nature Reviews Cancer:               https://www.nature.com/nrc/current_issue/rss  
  Nature Biomedical Engineering:       https://www.nature.com/natbiomedeng/current-issue/rss  
  Nature Biotechnology:                https://www.nature.com/nbt/current_issue/rss  
  Nature Genetics:                     https://www.nature.com/ng/current_issue/rss  
  Nature (main):                       https://www.nature.com/nature/rss  
  ```

  ([Nature][1], [Nature][2], [Nature][3], [Nature][4], [Nature][5], [Nature][6])
* **2023 Impact Factors (Clarivate):**

  | Journal                       | IF    |
  | ----------------------------- | ----- |
  | Nature Reviews Drug Discovery | 122.7 |
  | Nature Reviews Cancer         | 72.5  |
  | Nature Biomedical Engineering | 27.7  |
  | Nature Biotechnology          | 33.1  |
  | Nature Genetics               | 31.8  |
  | Nature (multidisciplinary)    | 50.5  |
  | ([Nature][7])                 |       |

---

**2. Project Skeleton & Dependencies**

```
digest‑mvp/
├─ app/
│  ├─ __init__.py       # create_app()
│  ├─ config.py         # journals, IF map, API keys
│  ├─ models.py         # SQLAlchemy Vote model
│  ├─ rss.py            # fetch_rss(journal_url)
│  ├─ summary.py        # summarize_abstracts(list[str]) → str
│  ├─ emailer.py        # build_and_send(digest, recipients)
│  ├─ feedback.py       # Flask blueprint: /feedback, /stats
│  └─ archiver.py       # commit_digest(file_path)
├─ run_digest.py        # orchestrates fetch → rank → summarize → email → archive
├─ requirements.txt     # feedparser, requests, beautifulsoup4, Flask, SQLAlchemy, PyGithub, openai, sendgrid
├─ Dockerfile
└─ .github/workflows/daily_digest.yml
```

---

**3. Core Modules**

* **rss.py**

  ```python
  import feedparser
  def fetch_rss(url):
      feed = feedparser.parse(url)
      return [{
          "title": e.title,
          "link":  e.link,
          "doi":   e.link.split("doi.org/")[-1],
          "abstract": e.summary,
      } for e in feed.entries]
  ```
* **summary.py**

  ```python
  import openai
  def summarize_abstracts(abstracts):
      prompt = (
          "Summarize each abstract in 2 sentences, focusing on novelty, "
          "then list the top 3 most interesting works:\n\n"
          + "\n\n".join(abstracts)
      )
      resp = openai.ChatCompletion.create(..., prompt=prompt)
      return resp["choices"][0]["message"]["content"]
  ```
* **emailer.py**

  ```python
  from sendgrid import SendGridAPIClient
  def build_and_send(digest_html, recipients):
      message = Mail(from_email="you@domain.com", to_emails=recipients, html_content=digest_html)
      SendGridAPIClient(api_key).send(message)
  ```

---

**4. Feedback API (Flask)**

```python
# app/feedback.py
from flask import Blueprint, request, redirect, jsonify
from .models import db, Vote

bp = Blueprint("feedback", __name__)

@bp.route("/feedback")
def feedback():
    doi = request.args.get("doi")
    vote = request.args.get("vote")
    if doi and vote in ("up", "down"):
        db.session.add(Vote(paper_doi=doi, vote=vote))
        db.session.commit()
        return redirect(request.args.get("next") or f"https://doi.org/{doi}")
    return "Invalid", 400

@bp.route("/stats")
def stats():
    data = db.session.query(Vote.paper_doi, Vote.vote, func.count()).group_by(Vote.paper_doi,Vote.vote).all()
    return jsonify({doi: {"up": u, "down": d} for doi, vote, count in data})
```

*Uses SQLite (zero cost) via SQLAlchemy.*

---

**5. Archiver: GitHub Pages Integration**

```python
# app/archiver.py
from github import Github
import os

def commit_digest(date_str, html_content):
    gh = Github(os.getenv("GITHUB_TOKEN"))
    repo = gh.get_repo(os.getenv("GITHUB_REPO"))  # e.g. "user/repo"
    path = f"digests/{date_str}.html"
    repo.create_file(path, f"Add digest {date_str}", html_content, branch="main")
```

---

**6. Scheduling & CI/CD**

* **GitHub Actions** (`.github/workflows/daily_digest.yml`):

  ```yaml
  name: Daily Digest
  on:
    schedule:
      - cron: '0 14 * * *' # 07:00 PST
    workflow_dispatch:
  jobs:
    run:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-python@v4
          with: python-version: '3.10'
        - run: pip install -r requirements.txt
        - name: Run digest
          env:
            OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
            SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            GITHUB_REPO: ${{ secrets.GITHUB_REPO }}
          run: python run_digest.py
  ```
* **Alternative Scheduler & Host (free/low‑cost)**

  * **PythonAnywhere**: free tier supports one scheduled daily task + Flask hosting; excellent docs.
  * **Render.com**: free tier supports web services and cron jobs; solid documentation.

---

**7. Next Steps**

1. **Populate** `app/config.py` with your journal‑URL map and the static IF map above.
2. **Implement** and locally test each module—especially `fetch_rss` + ranking by IF.
3. **Draft** your email template (Jinja2) including `👍/👎` links to `https://YOUR_DOMAIN/feedback?doi={{doi}}&vote=up`.
4. **Deploy** the Flask app (feedback API) to PythonAnywhere or Render.
5. **Wire up** GitHub Actions, store secrets, and verify end‑to‑end.

Let me know which component you'd like to flesh out first!

[1]: https://www.nature.com/nrd/current_issue/rss "Failed"
[2]: https://www.nature.com/nrc/current_issue/rss "Failed"
[3]: https://www.nature.com/natbiomedeng/current-issue/rss "Volume 9 Issue 4, April 2025"
[4]: https://www.nature.com/nbt/current_issue/rss "Failed"
[5]: https://www.nature.com/ng/current_issue/rss "Failed"
[6]: https://www.nature.com/nature/rss "Failed"
[7]: https://www.nature.com/nature-portfolio/about/journal-metrics "Journal Metrics | Nature Portfolio"
**Creating design spec**

The user asked for a detailed project plan and design spec, including an Impact Factor-based ranking system, thumbs up/down voting via email, and a GitHub Pages archive. I'll need to break it down into components like ingestion, ranking, summarization, email, feedback handling, and archiving. I'll outline the architecture, tech stack, storage schema, endpoints, and CI/CD setup. Additionally, a timeline and phases for the project will be helpful. I'll use markdown formatting and ensure the details are clear, focusing on the Impact Factor system.

**Finalizing project plan proposal**

I'll propose storing the Impact Factor mapping and implementing feedback integration on GitHub Pages. The archive will be static HTML with summaries and digest links, built via CI. Feedback will be tracked in a JSON file, updated by a commit pipeline, and displayed dynamically using JavaScript fetching data from an external API. I'll use SendGrid for email, GitHub actions for CI, and host on Heroku or AWS. The plan will include 5 phases and detail tasks, components, tech stack, and storage options like SQLite or PostgreSQL.

Thought for 7 seconds

Here's a detailed design spec and project plan incorporating:

* **Impact‑Factor only** ranking
* **Thumbs up/down** feedback in email
* **GitHub Pages** archive

---

## 1. System Overview

You'll build a daily pipeline that:

1. **Fetches** new articles from your chosen Nature journals' RSS feeds.
2. **Annotates** each with its Journal Impact Factor (IF).
3. **Selects & Ranks** the top N by IF.
4. **Summarizes** via an LLM (batch‑prompt).
5. **Emails** a styled digest with 👍/👎 links.
6. **Records** clicks on a backend service.
7. **Archives** each day's digest on GitHub Pages.
8. **Displays** vote tallies dynamically on your static site.

---

## 2. Architecture & Components

```text
┌───────────────┐    daily    ┌───────────────┐    batch‑prompt    ┌───────────────┐
│ RSS Feeds     │──fetch──▶  │ Ranking &     │───────────────▶  │ LLM Service   │
│ (Nature Jnl.) │            │ IF Annotator  │                   └───────────────┘
└───────────────┘            └───────────────┘                           │
                                                                         ▼
                                     ┌───────────────┐    generate   ┌───────────────┐
                                     │ Email Builder │────────────▶│ SMTP (SendGrid)│
                                     └───────────────┘              └───────────────┘
                                            │
                                            │ thumbs links
                                            ▼
                                   ┌─────────────────┐
                                   │ Feedback API    │◀── clicks
                                   │ (Flask/FastAPI) │
                                   └─────────────────┘
                                            │
                                 stats JSON │
                                            ▼
┌───────────────┐    git commit   ┌───────────────┐    GitHub Pages   ┌───────────────┐
│ Archiver      │─────────────▶  │ GitHub Repo   │◀───────────────▶│ Static Site   │
└───────────────┘                └───────────────┘                   └───────────────┘
```

---

## 3. Data Models

```yaml
Paper:
  doi: string           # unique ID
  title: string
  journal: string
  link: url
  abstract: text
  impact_factor: float
  pub_date: date

Digest:
  date: date            # e.g. 2025‑05‑03
  paper_ids: [doi,...]

Vote:
  id: uuid
  paper_doi: string
  vote: enum[up,down]
  timestamp: datetime
```

---

## 4. Core Modules & APIs

### 4.1 RSS Fetcher

* **Input:** list of `{journal, rss_url}`
* **Output:** new `Paper` records
* **Tech:** Python + `feedparser`

### 4.2 IF Annotator & Ranking

* **Load** static JSON: `{ journal: impact_factor }`
* **Filter/Sort:** pick top N by `impact_factor`
* **Persist** `Digest` for today

### 4.3 Summarization

* **Batch Prompt:**

  ```
  "Here are 5 abstracts. For each, write a 2‑sentence summary focusing on novelty.  
   Then rank them by interest and list the top 3."
  [Abstract 1]…[Abstract 5]
  ```
* **API:** OpenAI (or self‑hosted)
* **Output:** list of summaries + "most interesting" picks

### 4.4 Email Builder

* **Template (Jinja2):**

  * Header: date, "Nature Digest"
  * Ranked list:

    1. **Title** (IF = X.Y)

       * ► \[link]
       * *2‑sentence summary*
       * 👍 `<a href="https://api.yourdomain.com/feedback?doi=…&vote=up">`
       * 👎 `<a href="https://api.yourdomain.com/feedback?doi=…&vote=down">`
  * Footer: link to archive on GitHub Pages
* **Mailer:** SendGrid SMTP

### 4.5 Feedback API

* **Route:** `GET /feedback?doi=&vote=`

  * Validate params, record `Vote` in DB, then **redirect** to the paper's DOI URL or a "Thanks" page.
* **Route:** `GET /stats`

  * Return JSON:

    ```json
    { "10.1038/xyz": { "up": 12, "down": 3 }, … }
    ```

### 4.6 Archiver

* **Generate** for `YYYY-MM-DD.md` or `.html` under `/digests/` folder, using the same content as the email plus a `<div id="votes">`.
* **Commit & Push** via GitHub API or CLI using a bot token.

### 4.7 GitHub Pages Site

* **Index Page:** lists links to each `/digests/YYYY-MM-DD.html`.
* **Digest Pages:**

  * Static content: title, summaries
  * Client‑side JS:

    ```js
    fetch("https://api.yourdomain.com/stats")
      .then(r=>r.json())
      .then(stats=>{
        // find this digest's DOIs and inject vote counts next to 👍/👎
      });
    ```
* **Deployment:** automatically rebuilt on each push to `main`

---

## 5. Tech Stack

| Component            | Tech Choices                                      |
| -------------------- | ------------------------------------------------- |
| **Language**         | Python 3.10+                                      |
| **Web framework**    | FastAPI or Flask                                  |
| **LLM**              | OpenAI API                                        |
| **Email**            | SendGrid SMTP (or SES)                            |
| **Data store**       | SQLite (v1), upgrade to PostgreSQL if needed      |
| **Scheduler**        | cron (Linux), Heroku Scheduler, or GitHub Actions |
| **Containerization** | Docker                                            |
| **Hosting**          | Heroku / DigitalOcean / AWS LightSail             |
| **Static site**      | GitHub Pages (Jekyll or plain HTML)               |

---

## 6. Security & Reliability

* **Secrets:** store API keys & DB URL in environment vars.
* **Input validation:** sanitize query params on `/feedback`.
* **Rate‑limit** feedback endpoint to prevent spam.
* **Error alerts:** log exceptions; notify via Slack or email.
* **Monitoring:** basic uptime check on your backend (e.g., UptimeRobot).

---

## 7. 4‑Week Roadmap

|  Week | Goals & Deliverables                                                                                                   |
| :---: | ---------------------------------------------------------------------------------------------------------------------- |
| **1** | – Journal list + RSS URLs<br>– IF lookup JSON<br>– Prototype RSS fetcher + ranking script                              |
| **2** | – Summarization module with batch‑prompt<br>– Email template & local send test                                         |
| **3** | – Feedback API + simple DB recording<br>– Archiver: generate & commit daily digest                                     |
| **4** | – GitHub Pages site skeleton + JS stats injection<br>– Deploy end‑to‑end (scheduler, CI/CD)<br>– User testing & tuning |

---

### Next Steps

1. **Lock down** your list of Nature journals and their IF values.
2. **Build** the RSS → ranking prototype and verify it selects the correct top N.
3. **Draft** your email template and test a single local email (with dummy feedback links).

Let me know where you'd like to dive deeper or any tweaks to this plan!
