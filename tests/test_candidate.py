import logging
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

client = TestClient(app)

# Configure logger
logger = logging.getLogger("test-candidate")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def test_create_candidate():
    try:
        response = client.post("/api/candidates/", json={
            "name": "Gopal",
            "skills": [{"name": "Python", "expertise_level": 8}]
        })
        response.raise_for_status()
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Gopal"
        logger.info("test_create_candidate passed successfully.")

    except SQLAlchemyError as db_error:
        logger.error(f"Database error occurred: {db_error}")
        raise

    except ValidationError as val_error:
        logger.error(f"Validation error occurred: {val_error}")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
