# Candidate Grading System

## Project Overview

This is a FastAPI-based project for managing candidates and their project assignments. The system handles the CRUD operations for candidates, projects, and the associated skills.

## Steps to Run

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/candidate-grading-system.git
    cd candidate-grading-system
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Setup the PostgreSQL database and add the connection string in the `.env` file.

4. Run Alembic migrations:

    ```bash
    alembic upgrade head
    ```

5. Run the FastAPI server:

    ```bash
    uvicorn app.main:app --reload
    ```

6. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Testing

Run tests using `pytest`:

```bash
pytest
