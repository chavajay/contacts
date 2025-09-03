# Backend – FastAPI (Contacts Directory)

## Quickstart
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs on http://127.0.0.1:8000 (or http://localhost:8000). Interactive docs at `/docs`.

## Environment
- SQLite database at `app/contacts.db` (created automatically).
- CORS is open for local dev (`http://localhost:3000` by default for Nuxt).

## Notes
- Search is case-insensitive and matches name, email, phone, tag names, and note content.
- Simple change history is recorded for contact field updates (name, email, phone, favorite).
