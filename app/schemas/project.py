from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectSkillCreate(BaseModel):
    name: str
    expertise_level: int

class ProjectSkillRead(BaseModel):
    id: int
    name: str
    expertise_level: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    title: str
    skills: List[ProjectSkillCreate]


class ProjectRead(BaseModel):
    id: int
    title: str
    skills: List[ProjectSkillRead]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    skills: Optional[List[ProjectSkillCreate]] = None
    is_active: Optional[bool] = None
