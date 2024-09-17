from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models.project import Project, ProjectSkill
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.core.database import get_db
from app.core.logging_config import logger
from datetime import datetime
from typing import List

router = APIRouter()


@router.post("/", response_model=ProjectRead)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            new_project = Project(
                title=project.title,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(new_project)
            await db.flush()

            for skill in project.skills:
                new_skill = ProjectSkill(
                    name=skill.name,
                    expertise_level=skill.expertise_level,
                    project_id=new_project.id,
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_skill)

            await db.commit()

        return new_project

    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error creating project: {e}")


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Fetching project with id {project_id}")

        query = await db.execute(select(Project).where(Project.id == project_id))
        project = query.scalar_one_or_none()

        if not project:
            logger.warning(f"Project with id {project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")

        logger.info(f"Project fetched successfully: {project.id}")
        return project
    except Exception as e:
        logger.error(f"Error fetching project: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching project: {str(e)}")


@router.get("/active/", response_model=List[ProjectRead])
async def get_active_projects(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Fetching active projects, skip={skip}, limit={limit}")

        query = await db.execute(
            select(Project)
            .where(Project.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        projects = query.scalars().all()

        logger.info(f"Fetched {len(projects)} active projects")
        return projects
    except Exception as e:
        logger.error(f"Error fetching active projects: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching active projects: {str(e)}")


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, project_update: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Updating project with id {project_id}")

        query = await db.execute(select(Project).where(Project.id == project_id))
        project = query.scalar_one_or_none()

        if not project:
            logger.warning(f"Project with id {project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")

        update_data = project_update.dict(exclude_unset=True)

        if "skills" in update_data:
            logger.info(f"Updating skills for project id {project_id}")

            await db.execute(delete(ProjectSkill).where(ProjectSkill.project_id == project_id))

            project.skills = [ProjectSkill(
                name=skill.name,
                expertise_level=skill.expertise_level,
                project_id=project_id,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ) for skill in update_data["skills"]]

            del update_data["skills"]

        for key, value in update_data.items():
            setattr(project, key, value)

        project.updated_at = datetime.utcnow()
        db.add(project)

        async with db.begin():
            await db.commit()
            await db.refresh(project)

        logger.info(f"Project updated successfully: {project.id}")
        return project
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error updating project: {str(e)}")


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Soft deleting project with id {project_id}")

        query = await db.execute(select(Project).where(Project.id == project_id))
        project = query.scalar_one_or_none()

        if not project:
            logger.warning(f"Project with id {project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")

        project.is_active = False
        project.updated_at = datetime.utcnow()
        db.add(project)

        async with db.begin():
            await db.commit()

        logger.info(f"Project {project_id} soft-deleted successfully")
        return {"message": "Project soft-deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error deleting project: {str(e)}")
