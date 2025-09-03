from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class ContactTagLink(SQLModel, table=True):
    contact_id: Optional[int] = Field(default=None, foreign_key="contact.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    favorite: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    notes: List["Note"] = Relationship(back_populates="contact")
    tags: List["Tag"] = Relationship(back_populates="contacts", link_model=ContactTagLink)

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: int = Field(foreign_key="contact.id", index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    contact: Optional[Contact] = Relationship(back_populates="notes")

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    contacts: List[Contact] = Relationship(back_populates="tags", link_model=ContactTagLink)

class ChangeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: int = Field(foreign_key="contact.id", index=True)
    field: str
    old_value: str
    new_value: str
    changed_at: datetime = Field(default_factory=datetime.utcnow)
