from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select, or_, col
from ..database import get_session
from ..models import Contact, Note, Tag, ChangeLog
from ..schemas import ContactCreate, ContactRead, ContactUpdate, NoteCreate, NoteRead, ChangeLogRead
from ..utils import diff_fields
from datetime import datetime

router = APIRouter(prefix="/contacts", tags=["contacts"])

def _upsert_tags(session: Session, tag_names: List[str]) -> List[Tag]:
    tags = []
    for name in set([t.strip() for t in tag_names if t.strip()]):
        tag = session.exec(select(Tag).where(Tag.name == name)).first()
        if not tag:
            tag = Tag(name=name)
            session.add(tag)
            session.flush()
        tags.append(tag)
    return tags

@router.get("", response_model=List[ContactRead])
def list_contacts(
    q: Optional[str] = Query(default=None, description="Search by name,email,phone,tag,note"),
    favorite: Optional[bool] = None,
    tag: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    stmt = select(Contact).order_by(Contact.updated_at.desc())

    if favorite is not None:
        stmt = stmt.where(Contact.favorite == favorite)

    if tag:
        stmt = stmt.join(Contact.tags).where(Tag.name == tag)

    if q:
        like = f"%{q.lower()}%"

        stmt = (
            stmt.outerjoin(Contact.notes)
                .outerjoin(Contact.tags)
                .where(
                    or_(
                        col(Contact.name).ilike(like),
                        col(Contact.email).ilike(like),
                        col(Contact.phone).ilike(like),
                        col(Tag.name).ilike(like),
                        col(Note.content).ilike(like),
                    )
                )
            .distinct()
        )

    stmt = stmt.limit(limit).offset(offset)
    contacts = session.exec(stmt).all()

    result = []
    for c in contacts:
        result.append(ContactRead(
            id=c.id, name=c.name, email=c.email, phone=c.phone, favorite=c.favorite,
            tags=[t.name for t in c.tags],
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat(),
        ))
    return result

@router.post("", response_model=ContactRead, status_code=201)
def create_contact(payload: ContactCreate, session: Session = Depends(get_session)):
    contact = Contact(name=payload.name, email=payload.email, phone=payload.phone, favorite=bool(payload.favorite))
    if payload.tags:
        contact.tags = _upsert_tags(session, payload.tags)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return ContactRead(
        id=contact.id, name=contact.name, email=contact.email, phone=contact.phone, favorite=contact.favorite,
        tags=[t.name for t in contact.tags], created_at=contact.created_at.isoformat(),
        updated_at=contact.updated_at.isoformat()
    )

@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(contact_id: int, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactRead(
        id=contact.id, name=contact.name, email=contact.email, phone=contact.phone, favorite=contact.favorite,
        tags=[t.name for t in contact.tags], created_at=contact.created_at.isoformat(),
        updated_at=contact.updated_at.isoformat()
    )

@router.patch("/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, payload: ContactUpdate, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    before = {
        "name": contact.name, "email": contact.email, "phone": contact.phone, "favorite": contact.favorite
    }
    if payload.name is not None:
        contact.name = payload.name
    if payload.email is not None:
        contact.email = payload.email
    if payload.phone is not None:
        contact.phone = payload.phone
    if payload.favorite is not None:
        contact.favorite = payload.favorite
    if payload.tags is not None:
        contact.tags = _upsert_tags(session, payload.tags)

    contact.updated_at = datetime.utcnow()

    # historial de cambios
    after = {
        "name": contact.name, "email": contact.email, "phone": contact.phone, "favorite": contact.favorite
    }
    for f, old, new in diff_fields(before, after, ["name", "email", "phone", "favorite"]):
        session.add(ChangeLog(contact_id=contact.id, field=f, old_value=str(old), new_value=str(new)))

    session.add(contact)
    session.commit()
    session.refresh(contact)
    return ContactRead(
        id=contact.id, name=contact.name, email=contact.email, phone=contact.phone, favorite=contact.favorite,
        tags=[t.name for t in contact.tags], created_at=contact.created_at.isoformat(),
        updated_at=contact.updated_at.isoformat()
    )

@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(contact)
    session.commit()
    return

@router.post("/{contact_id}/notes", response_model=NoteRead, status_code=201)
def add_note(contact_id: int, payload: NoteCreate, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    note = Note(contact_id=contact_id, content=payload.content)
    session.add(note)
    session.commit()
    session.refresh(note)
    return NoteRead(id=note.id, content=note.content, created_at=note.created_at.isoformat())

@router.get("/{contact_id}/notes", response_model=List[NoteRead])
def list_notes(contact_id: int, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    notes = session.exec(select(Note).where(Note.contact_id == contact_id).order_by(Note.created_at.desc())).all()
    return [NoteRead(id=n.id, content=n.content, created_at=n.created_at.isoformat()) for n in notes]

@router.delete("/{contact_id}/notes/{note_id}", status_code=204)
def delete_note(contact_id: int, note_id: int, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    note = session.get(Note, note_id)
    if not note or note.contact_id != contact_id:
        raise HTTPException(status_code=404, detail="Note not found")
    
    session.delete(note)
    session.commit()
    return

@router.get("/{contact_id}/history", response_model=List[ChangeLogRead])
def get_history(contact_id: int, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    logs = session.exec(select(ChangeLog).where(ChangeLog.contact_id == contact_id).order_by(ChangeLog.changed_at.desc())).all()
    return [ChangeLogRead(id=l.id, field=l.field, old_value=l.old_value, new_value=l.new_value, changed_at=l.changed_at.isoformat()) for l in logs]
