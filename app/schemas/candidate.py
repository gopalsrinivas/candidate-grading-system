from pydantic import BaseModel
from typing import List


class CandidateSkillSchema(BaseModel):
    name: str
    expertise_level: int


class CandidateCreateSchema(BaseModel):
    name: str
    skills: List[CandidateSkillSchema]


class CandidateUpdateSchema(BaseModel):
    name: str
    skills: List[CandidateSkillSchema]
