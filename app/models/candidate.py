from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
import pytz

class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    expertise_level: int

class Candidate(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    skills: list[Skill] = Relationship(back_populates="candidate")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
