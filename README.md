# ToolRank — AI Tool Review Platform

A Yelp-style platform for discovering and reviewing AI tools.
Built with **Python Bottle** + **PostgreSQL** for a Databases final project.

---

## Features

- **Browse & Search** AI tools by name, category, or audience type
- **User accounts** with registration / login
- **Star ratings** — overall and per-category (Ease of Use, Accuracy, Value, Creativity, Support)
- **Written reviews** with versioning (edit your review; history preserved)
- **Audience tags** — TODO
- **Review voting** — upvote / downvote helpful reviews
- **Bookmarks** — save tools to your profile
- **Submit new tools** — any logged-in user can add a tool

---

## Setup

### 1. Install dependencies
```bash
pip install bottle
pip install psycopg2
```


### 2. Run the app
```bash
python app.py
```

Open **http://localhost:8080** in your browser.

---

## Project Structure

```
aitool_reviewer/
├── app.py                  # All routes, DB helpers, auth logic (Bottle)
├── templates/
│   ├── base.tpl            # Shared navbar / footer layout
│   ├── index.tpl           # Home page
│   ├── search.tpl          # Search & filter results
│   ├── tool_detail.tpl     # Tool page with reviews & review form
│   ├── register.tpl        # Sign-up page
│   ├── login.tpl           # Login page
│   ├── profile.tpl         # User profile + bookmarks
│   └── add_tool.tpl        # Submit a new tool
├── static/
│   ├── css/style.css       # All styles
│   └── js/main.js          # Star picker interaction
└── backend/                # Database setup layer (does not run as part of the app)
    ├── models.py           # SQLAlchemy ORM models defining the full database schema
    ├── extensions.py       # SQLAlchemy instance used by the models
    ├── populate_db.py      # Seeds the Neon PostgreSQL database with initial data
    ├── app.py              # Minimal Flask context required to run populate_db.py
    └── SystemDesign.md     # Original schema design notes
```

> **Note:** The `backend/` folder was used solely to design the database schema and seed it in Neon.
> It does **not** interact with the Bottle application (`app.py`) at runtime.
> The running app connects to the already-provisioned Neon database directly via psycopg2.

---

## Database Schema

| Table            | Purpose                                              |
|------------------|------------------------------------------------------|
| `Users`          | Accounts with username, email                        |
| `AI_Tools`       | Tool catalogue (name, company, category, price, avg rating) |
| `Reviews`        | User reviews with versioning support                 |
| `Topical_Reviews`| Per-category sub-ratings linked to a review version  |
| `Tags`           | Audience tags on tools (set when a typed user reviews) |
| `Bookmarks`      | Saved tools per user                                 |
| `Review_Votes`   | Upvote / downvote on reviews                         |

---
