# LinkedIn Scraping Worker

A task-driven Python worker that scrapes LinkedIn at scale using Selenium. Tasks are read from a **Firestore queue**, dispatched to the appropriate scraper based on task category, and results are written back to Firestore. Supports both standard LinkedIn and **Sales Navigator**.

---

## What it does

The worker runs in a continuous loop, picking up batches of scraping jobs from Firestore and routing each one to the right handler:

| Task category | What gets scraped |
|---|---|
| `about` | LinkedIn company About page (overview, size, industry, HQ, founded year…) |
| `numerical_about` | Same as above, but identified by numeric LinkedIn ID |
| `ppl` | LinkedIn person profile (experience, education, contact info) |
| `search_people` | Standard LinkedIn people search results |
| `search_people_advanced` | Sales Navigator people search with filters (title, company, location, school…) |
| `get_profile_search_people_advanced` | Full profile from a Sales Navigator people search result |
| `search_companies_advanced` | Sales Navigator company search |
| `get_profile_search_company_advanced` | Full profile from a Sales Navigator company search result |
| `25_months_employees` | 25-month employee headcount history for a company |
| `sn_employees_movements` | Employee movement data via Sales Navigator |
| `sn_ppl` | Raw HTML download of a Sales Navigator profile page |
| `check_html` | Health check — verifies the scraper still returns valid data |

---

## Architecture

```
Firestore (task queue)
        │
        ▼
   Worker.__call__()          ← continuous polling loop
        │
        ▼
   __process_task()           ← routes by task["category"]
        │
   ┌────┴──────────────────────────────────────┐
   │  __process_about()                        │
   │  __process_ppl()                          │
   │  __process_advanced_search_ppl()          │  ← each calls its
   │  __process_advanced_search_company()      │     scraping module
   │  __process_25_months_employees()          │
   │  ...                                      │
   └───────────────────────────────────────────┘
        │
        ▼
  Scraping modules (Selenium)
        │
        ▼
  Firestore (results + task status update)
```

Tasks are prioritised by `t_priority` then `updated` timestamp. After a task completes, its status is updated to `processed_success` or `processed_failure` and it is removed from the worker's queue.

---

## Tech stack

- **Python 3.10+**
- **Selenium** — browser automation for LinkedIn scraping
- **Firebase Admin SDK** — Firestore task queue and result storage
- **Google Firestore** — distributed task queue + data store

---

## Project structure

```
linkedin-scraping-worker/
├── worker.py                     # Main worker class and task dispatcher
├── abouts.py                     # Scrapes LinkedIn company About pages
├── ppl_info_old.py               # Scrapes LinkedIn person profiles
├── search_ppl.py                 # Standard LinkedIn people search
├── advanced_search_ppl.py        # Sales Navigator people search
├── advanced_search_companies.py  # Sales Navigator company search
├── advanced_profiles_html.py     # Full profile fetch from SN search results
├── insights.py                   # 25-month headcount history
├── downloadhtml.py               # Sales Navigator profile HTML downloader
├── sn_employees_movements.py     # Employee movement data via SN
├── getnumericals.py              # Scrapes by numeric LinkedIn ID
├── save_website.py               # Domain extraction utility
├── utils.py                      # LinkedIn login/logout, shared helpers
├── config.example.json           # Example config (no real credentials)
├── requirements.txt
└── .gitignore
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/JoyMikhaelLeb/LI-scraper-selen.git
cd LI-scraper-selen
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Add your Firestore service account key**

Download your Firebase service account JSON from the Firebase console and place it somewhere outside the repo (never commit it).

**4. Configure the worker**

Copy the example config and fill in your values:
```bash
cp config.example.json workers/my_worker.json
```

```json
{
    "firestore_certificate": "/path/to/serviceAccount.json",
    "email": "your-linkedin-account@example.com",
    "headless_chrome": true,
    "batch_size": 5,
    "log_level": "info"
}
```

**5. Run the worker**
```bash
python worker.py workers/my_worker.json
```

---

## Configuration reference

| Key | Type | Description |
|---|---|---|
| `firestore_certificate` | string | Absolute path to the Firebase service account JSON |
| `email` | string | LinkedIn account the worker will log in with |
| `headless_chrome` | bool | Run Chrome without a visible window |
| `batch_size` | int | Number of tasks to fetch per polling cycle |
| `log_level` | string | `info`, `debug`, or `warning` |

---

## Key design decisions

**Task queue over direct calls** — tasks are written to Firestore by a separate orchestrator. The worker only reads and executes, which makes it easy to scale horizontally (multiple workers, each with its own LinkedIn account).

**Validation detection** — LinkedIn occasionally challenges accounts with a security checkpoint. The worker detects this, updates its status in Firestore to `needs validation`, re-queues all pending tasks, and exits cleanly so the account isn't locked out.

**Staleness checks** — before re-scraping, the worker checks whether the stored data is already fresh (collected today or yesterday). This avoids unnecessary requests and reduces the risk of rate limiting.

**Batch status updates** — when a result is already cached (same target, same category), all duplicate queued tasks are marked `processed_success` in a single Firestore batch write instead of re-running the scraper for each one.

---

## Notes

- This project was built for a client data pipeline. The repository contains the scraping worker only — the orchestration layer (task creation, scheduling) and the downstream data processing are not included.
- A real LinkedIn account with Sales Navigator access is required for `search_people_advanced`, `search_companies_advanced`, `sn_ppl`, and `sn_employees_movements` tasks.
