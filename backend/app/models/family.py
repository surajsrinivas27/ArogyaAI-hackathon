from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4


class FamilyMemberCreate(BaseModel):
    name: str
    age: int
    gender: str
    blood_group: str
    relationship: str
    allergies: Optional[str] = ""
    medical_conditions: Optional[str] = ""


class FamilyMemberInDB(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    owner_email: str
    name: str
    age: int
    gender: str
    blood_group: str
    relationship: str
    allergies: str = ""
    medical_conditions: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)