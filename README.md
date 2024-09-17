# candidate-grading-system

### 5. `README.md`
A simple README for the project.

```md
# Candidate Grading System

This is a backend system built using FastAPI for managing candidates and their associated projects and skills.

## Key Features

- Create, update, and manage candidates and their skillsets.
- Manage projects and their required skills.
- PostgreSQL used as the primary database.
- Alembic is used for database migrations.
- Logging and error handling are implemented for robust API operations.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/candidate-grading-system.git
    ```

2. Navigate into the project directory:

    ```bash
    cd candidate-grading-system
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file with the following contents:

    ```env
    DATABASE_URL=postgresql://your_user:your_password@localhost/your_db_name
    SECRET_KEY=your_secret_key
    DEBUG=True
    ```

5. Set up the PostgreSQL database, then run migrations:

    ```bash
    alembic upgrade head
    ```

6. Run the development server:

    ```bash
    uvicorn app.main:app --reload
    ```

7. Open the API documentation:

    [http://localhost:8000/docs](http://localhost:8000/docs)

## License

MIT License
