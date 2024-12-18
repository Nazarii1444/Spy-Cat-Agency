# Spy Cat Agency API

## Overview

The Spy Cat Agency API is designed to manage spy cats, their missions, and targets efficiently. This API allows:

- Managing spy cats (CRUD operations).
- Creating missions and assigning them to spy cats.
- Adding targets to missions.
- Updating and retrieving mission and target details.

This documentation provides an overview of how to set up and use the API.

---

## Requirements

- Python 3.9+
- FastAPI
- SQLAlchemy
- SQLite (default database)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Nazarii1444/Spy-Cat-Agency.git
```
   
2. Set up a virtual environment and install dependencies:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn main:app --reload
```
or simply run app.py file.

4. Access the API documentation

```bash
Open http://127.0.0.1:8000/docs for Swagger UI.
Open http://127.0.0.1:8000/redoc for ReDoc.
```

