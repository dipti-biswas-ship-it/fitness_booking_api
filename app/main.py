from .routes import router as booking_router
from fastapi import FastAPI
from . import models
from .database import engine

# Automatically create tables in the database using SQLAlchemy models
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI(title="Fitness Booking API")

# Include the booking routes (class and booking endpoints)
app.include_router(booking_router)