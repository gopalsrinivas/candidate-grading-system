from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.candidate import Candidate, CandidateSkill
from app.schemas.candidate import CandidateSchema, ShowCandidateSchema
from app.core.logging_config import logger

router = APIRouter()

@router.post("/candidates/", response_model=ShowCandidateSchema)
async def create_candidate(candidate: CandidateSchema, db: Session = Depends(get_db)):
    try:
        db_candidate = Candidate(name=candidate.name, is_active=True)
        for skill in candidate.skills:
            db_candidate.skills.append(CandidateSkill(
                name=skill.name, expertise_level=skill.expertise_level))
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        return db_candidate
    except Exception as e:
        logger.error(f"Error creating candidate: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/candidates/{candidate_id}", response_model=ShowCandidateSchema)
async def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    try:
        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id, Candidate.is_active == True).first()
        if not candidate:
            raise HTTPException(
                status_code=404, detail="Candidate not found or inactive")
        return candidate
    except Exception as e:
        logger.error(f"Error retrieving candidate with ID {candidate_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/candidates/", response_model=list[ShowCandidateSchema])
async def get_active_candidates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        candidates = db.query(Candidate).filter(
            Candidate.is_active == True).offset(skip).limit(limit).all()
        return candidates
    except Exception as e:
        logger.error(f"Error retrieving candidates: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/candidates/{candidate_id}", response_model=ShowCandidateSchema)
async def update_candidate(candidate_id: int, updated_candidate: CandidateSchema, db: Session = Depends(get_db)):
    try:
        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id, Candidate.is_active == True).first()
        if not candidate:
            raise HTTPException(
                status_code=404, detail="Candidate not found or inactive")

        candidate.name = updated_candidate.name
        candidate.skills = [CandidateSkill(
            name=skill.name, expertise_level=skill.expertise_level) for skill in updated_candidate.skills]
        db.commit()
        return candidate
    except Exception as e:
        logger.error(f"Error updating candidate with ID {candidate_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    try:
        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        candidate.is_active = False
        db.commit()
        return {"detail": "Candidate deactivated"}
    except Exception as e:
        logger.error(f"Error deleting candidate with ID {candidate_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
