import logging
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

client = TestClient(app)

# Configure logger
logger = logging.getLogger("test-project")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def test_create_project():
    try:
        response = client.post("/api/projects/", json={
            "title": "FastAPI Project",
            "skills": [{"name": "SQLAlchemy", "expertise_level": 4}]
        })
        response.raise_for_status()
        data = response.json()

        assert response.status_code == 200
        assert data["title"] == "FastAPI Project"
        logger.info("test_create_project passed successfully.")

    except SQLAlchemyError as db_error:
        logger.error(f"Database error occurred: {db_error}")
        raise

    except ValidationError as val_error:
        logger.error(f"Validation error occurred: {val_error}")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
