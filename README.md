Thought for a couple of seconds


Here’s a lean, end‑to‑end design for your “daily digest” MVP with Flask + GitHub Pages + OpenAI:

---

## 1. Goals & Scope

1. **Daily fetch** of today’s articles from your selected Nature journals via RSS.
2. **Flask app** generates a single HTML page listing:

   * Article **title** (linked to its DOI)
   * Auto‑generated **2‑sentence summary** via OpenAI
3. **Re‑rank** the list by a second OpenAI call that takes a plain‑text “preferences” file and returns a reordered list of DOIs.
4. **Publish** the resulting HTML to GitHub Pages under `/digests/YYYY-MM-DD.html`.

All else (feedback buttons, vote tracking, email, IF‑filtering) is out of MVP scope.

---

## 2. High‑Level Architecture

```text
┌──────────────┐       ┌───────────────┐       ┌───────────────┐       ┌─────────────┐
│  RSS Feeds   │─fetch─▶│ Flask App     │─calls─▶│ OpenAI ①      │─summaries─▶│ HTML Builder│
└──────────────┘       └───────────────┘       └───────────────┘       └─────────────┘
                                                   │                               │
                                                   │                               ▼
                                                   │                          ┌───────────────┐
                                                   │ rankings via OpenAI ②     │ GitHub Commit │
                                                   └──────────────────────────▶│ (Pages)       │
                                                                               └───────────────┘
```

---

## 3. Directory Layout

```
digest‑mvp/
├─ app/
│  ├─ __init__.py          # create_app()
│  ├─ config.py            # RSS URLs + prefs file path + GitHub info
│  ├─ fetcher.py           # fetch_today_articles() → List[Paper]
│  ├─ summarizer.py        # summarize_papers(papers) → adds .summary
│  ├─ ranker.py            # rank_papers(papers) → reordered list
│  ├─ renderer.py          # render_digest(date, papers) → HTML str
│  └─ github_uploader.py   # push_to_github(path, content)
├─ preferences.txt         # user’s text description of interests
├─ run.py                  # orchestration script (can also be Flask CLI)
├─ requirements.txt        # Flask, feedparser, openai, PyGithub, Jinja2
└─ .github/workflows/ci.yml # optional: GitHub Actions for daily run
```

---

## 4. Core Components

### 4.1 `config.py`

```python
RSS_FEEDS = {
  "Nature Reviews Drug Discovery": "https://www.nature.com/nrd/current_issue/rss",
  …  
}
PREFERENCES_FILE = "preferences.txt"
GITHUB_REPO = "username/repo"       # your Pages repo
GITHUB_BRANCH = "main"
DIGEST_PATH_FMT = "digests/{date}.html"
OPENAI_MODEL = "gpt-4.1-mini"
```

### 4.2 `fetcher.py`

* **Function:** `fetch_today_articles()`
* **Logic:**

  1. Pull each feed with `feedparser`.
  2. Filter entries where `published` == today’s date.
  3. Build `Paper` objects: `{ doi, title, link, abstract }`.

### 4.3 `summarizer.py`

* **Function:** `summarize_papers(papers: List[Paper])`
* **Implementation:**

  ```python
  prompts = [
    f"Abstract: {p.abstract}\n\nPlease summarize in two sentences focusing on its key novelty."
    for p in papers
  ]
  # You can batch multiple prompts in one chat completion if under token limit.
  responses = openai.ChatCompletion.create(
    model=OPENAI_MODEL,
    messages=[{"role":"system","content":"You are a concise science summarizer."}]
             + [{"role":"user","content":pr} for pr in prompts]
  )
  # Map responses back to papers[i].summary
  ```

### 4.4 `ranker.py`

* **Function:** `rank_papers(papers: List[Paper]) -> List[Paper]`
* **Implementation:**

  ```python
  prefs = open("preferences.txt").read()
  doi_list = [p.doi for p in papers]
  prompt = (
    "Here is a user’s preferences:\n"
    f"{prefs}\n\n"
    "Please order the following DOIs by how well they match these preferences, best first:\n"
    + "\n".join(doi_list)
  )
  resp = openai.ChatCompletion.create(
    model=OPENAI_MODEL,
    messages=[{"role":"user","content":prompt}]
  )
  ordered = parse_list_from_text(resp.choices[0].message.content)
  # Return [paper for doi in ordered for paper in papers if paper.doi==doi]
  ```

### 4.5 `renderer.py`

* **Function:** `render_digest(date: str, papers: List[Paper]) -> str`
* **Implementation:** Jinja2 template:

  ```html
  <!DOCTYPE html><html><head><meta charset="utf-8"><title>{{date}} Digest</title></head>
  <body>
    <h1>{{date}} Nature Digest</h1>
    {% for p in papers %}
      <div class="paper">
        <h2><a href="{{p.link}}">{{p.title}}</a></h2>
        <p><em>DOI: {{p.doi}}</em></p>
        <p>{{p.summary}}</p>
      </div>
      <hr/>
    {% endfor %}
  </body></html>
  ```

### 4.6 `github_uploader.py`

* **Function:** `push_to_github(path: str, content: str)`
* **Implementation:** PyGithub:

  ```python
  from github import Github
  gh = Github(os.getenv("GITHUB_TOKEN"))
  repo = gh.get_repo(config.GITHUB_REPO)
  repo.create_file(
    path, f"Add digest {date}", content, branch=config.GITHUB_BRANCH
  )
  ```

---

## 5. Orchestration (`run.py`)

```python
from app.fetcher import fetch_today_articles
from app.summarizer import summarize_papers
from app.ranker import rank_papers
from app.renderer import render_digest
from app.github_uploader import push_to_github
from datetime import date

def main():
    today = date.today().isoformat()
    papers = fetch_today_articles()
    summarize_papers(papers)
    papers = rank_papers(papers)
    html = render_digest(today, papers)
    path = config.DIGEST_PATH_FMT.format(date=today)
    push_to_github(path, html)

if __name__=="__main__":
    main()
```

---

## 6. Scheduling

* **GitHub Actions**: add a workflow to run `python run.py` at `0 14 * * *` (07:00 PST).
* **Alternative**: a cheap VPS + cron, or PythonAnywhere’s free scheduled task.

---

## 7. Next Steps

1. **Bootstrap** the repo with this structure + empty modules.
2. **Implement & test** `fetcher.py` → confirm today’s articles.
3. **Wire up** `summarizer.py` with dummy abstracts.
4. **Draft** `preferences.txt` with your top‑of‑mind fields (“synthetic biology, drug delivery, …”).
5. **Build** `ranker.py` and verify it reorders a sample DOI list.
6. **Hook up** `renderer.py` and manually push one digest to GitHub Pages.

Once each piece works end‑to‑end, you’ll have a working MVP you can iterate on (adding IF‑filtering, email delivery, feedback, etc.). Let me know where you’d like to dive in first!
