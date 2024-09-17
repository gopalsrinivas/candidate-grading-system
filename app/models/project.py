from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    skills: List["ProjectSkill"] = Relationship(back_populates="project")


class ProjectSkill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    expertise_level: int
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    project: Optional[Project] = Relationship(back_populates="skills")


class ProjectSkillCreate(SQLModel):
    name: str
    expertise_level: int


class ProjectCreate(SQLModel):
    title: str
    skills: List[ProjectSkillCreate]


class ProjectRead(SQLModel):
    id: int
    title: str
    skills: List[ProjectSkillCreate]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    skills: Optional[List[ProjectSkillCreate]] = None
