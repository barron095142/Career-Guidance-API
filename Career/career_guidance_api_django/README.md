# Career Guidance API (Django + DRF)

A lightweight, battery‑included backend for your Career Guidance app with:

- Sign up / Login (JWT)
- AI Chat (OpenRouter / ChatGPT‑5)
- Daily Rate Limiting (5 calls/user/day by default)
- Roadmap, Job‑Market, Skills, Recommendations, Career Paths, Interview, Resume (stubbed endpoints you can extend)

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (optional) copy .env.example to .env and fill in keys OR export vars in shell
export OPENROUTER_API_KEY=sk-or-xxxxxxxx

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Default Config
- Daily limit: `DAILY_API_LIMIT=5`
- Timezone: Australia/Sydney
- CORS: open for dev

## API Overview

### Auth
- **POST** `/api/auth/signup/` → `{username, first_name, last_name, password, phone_number}`
- **POST** `/api/auth/login/` → `{username, password}` → returns `{access, refresh}`

Use the `access` token as `Authorization: Bearer <token>` for protected endpoints.

### Rate Limiting
- **GET** `/api/rate/status/` → `{count, remaining, limit, reached}`
- **POST** `/api/rate/hit/` → increments and returns the same payload

> The chat endpoint also enforces the limit and increments after a successful reply.

### AI Chat
- **POST** `/api/ai/chat/` body: `{"query":"Your question"}` → `{response, usage}`

### Domain Services (stubs to extend)
- **GET** `/api/roadmap/?role=software engineer`
- **GET** `/api/job-market/?city=Sydney&role=software engineer`
- **POST** `/api/skills/analyze/` body: `{text}`
- **GET** `/api/recommendations/?skills=python,react`
- **GET** `/api/career/paths/?skills=python,react`
- **POST** `/api/interview/qa/` body: `{role}`
- **POST** `/api/resume/score/` body: `{text}`

### Optional News Helper
- **GET** `/api/news/` (no auth) – pulls AU headlines if `NEWS_API_KEY` set.

## Notes
- Custom user extends Django `AbstractUser` with `phone_number`.
- JWT via `djangorestframework-simplejwt`.
- Rate table: `APICallCounter(user, date, count)` with one row per user per day.
- You can also call `/api/rate/hit/` from the frontend whenever you want to count a call outside of `/api/ai/chat/`.
