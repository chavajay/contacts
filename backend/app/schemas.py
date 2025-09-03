from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, constr

PhoneStr = constr(pattern=r"^[+]?\d[\d\s-]{6,16}\d$")

class NoteCreate(BaseModel):
    content: constr(min_length=1, max_length=2000)

class NoteRead(BaseModel):
    id: int
    content: str
    created_at: str

class TagCreate(BaseModel):
    name: constr(min_length=1, max_length=40)

class TagRead(BaseModel):
    id: int
    name: str

class ContactBase(BaseModel):
    name: constr(min_length=1, max_length=120)
    email: EmailStr
    phone: PhoneStr
    favorite: Optional[bool] = False
    tags: Optional[List[str]] = Field(default_factory=list)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=120)] = None
    email: Optional[EmailStr] = None
    phone: Optional[PhoneStr] = None
    favorite: Optional[bool] = None
    tags: Optional[List[str]] = None

class ContactRead(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    favorite: bool
    tags: List[str]
    created_at: str
    updated_at: str

class ChangeLogRead(BaseModel):
    id: int
    field: str
    old_value: str
    new_value: str
    changed_at: str
