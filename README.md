### Fitness Booking API

A RESTful API for managing fitness classes and bookings, built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**. This project supports timezone-aware scheduling and includes a complete setup guide for local development.

---

---
## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dipti-biswas-ship-it/fitness_booking_api.git
cd fitness_booking_api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

###  .env Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/yourdbname
TIMEZONE=Asia/Kolkata

###  Set Up database PostgreSQL
CREATE DATABASE your_database_name;


### Run Alembic Migrations
alembic init alembic      # Run only once if not already initialized
alembic revision --autogenerate -m "init"
alembic upgrade head

### Run 
uvicorn app.main:app --reload