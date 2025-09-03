# Contacts Directory (SPA + API)

Stack:
- **Frontend**: Nuxt 3 + Ionic Vue + Pinia + TypeScript
- **Backend**: FastAPI + SQLModel (SQLite)

## Run locally
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
pnpm i  # or npm i / yarn
pnpm dev
```

Then open http://localhost:3000

## Notes
- You can inspect the API docs at http://127.0.0.1:8000/docs
- DB file persists at `backend/app/contacts.db`.
- Field validations exist both in frontend (Zod) and backend (Pydantic).
