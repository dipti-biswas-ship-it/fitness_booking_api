
# from .database import engine, Base, SessionLocal
from .routes import router as booking_router
from fastapi import FastAPI
from . import models
from .database import engine
# Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Fitness Booking API")
app.include_router(booking_router)

