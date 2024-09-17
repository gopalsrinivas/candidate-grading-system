from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import project
from app.core.database import engine, SQLModel
from app.core.logging_config import logger

app = FastAPI(
    title="Candidate Grading System",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router, prefix="/api/projects", tags=["projects"])
app.include_router(project.router, prefix="/api/candidates", tags=["candidates"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application and creating database tables.")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        tables = SQLModel.metadata.tables
        logger.info(f"Tables created: {list(tables.keys())}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
