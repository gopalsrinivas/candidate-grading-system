from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.models.project import Project
from app.models.candidate import Candidate
from app.core.logging_config import logger

router = APIRouter()

@router.post("/form-team/")
async def form_team(project_id: int, candidate_ids: List[int], team_size: int, db: AsyncSession = Depends(get_db)):
    try:
        project = await db.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        candidates = await db.execute(
            db.query(Candidate).filter(Candidate.id.in_(candidate_ids))
        )
        candidates = candidates.scalars().all()

        return {
            "team": [],  # The optimal team
            "total_expertise": 0,
            "coverage": 1.0
        }
    except Exception as e:
        logger.error(f"Error forming team for project ID {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
