# Frontend – Nuxt 3 + Ionic Vue (SPA)

## Quickstart
```bash
cd frontend
pnpm i # or npm i / yarn
pnpm dev
```

The app runs at `http://localhost:3000` and expects the API at `http://127.0.0.1:8000` by default.
To point to a different API base, set `NUXT_PUBLIC_API_BASE` env var.

## Features
- Real-time search (debounced) across name/email/phone/tags/notes
- CRUD contacts with validation (email + phone patterns)
- Notes per contact
- Favorites and tags
- Change history viewer
- Clean Ionic design
