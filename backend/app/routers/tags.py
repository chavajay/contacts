from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_session
from ..models import Tag, Contact
from ..schemas import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("", response_model=List[TagRead])
def list_tags(session: Session = Depends(get_session)):
    tags = session.exec(select(Tag).order_by(Tag.name.asc())).all()
    return [TagRead(id=t.id, name=t.name) for t in tags]

@router.post("", response_model=TagRead, status_code=201)
def create_tag(payload: TagCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Tag).where(Tag.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag = Tag(name=payload.name)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return TagRead(id=tag.id, name=tag.name)
