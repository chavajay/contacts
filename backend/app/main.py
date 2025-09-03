from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers.contacts import router as contacts_router
from .routers.tags import router as tags_router

init_db()
app = FastAPI(title="Contacts Directory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts_router)
app.include_router(tags_router)

@app.get("/health")
def health():
    return {"status": "ok"}
