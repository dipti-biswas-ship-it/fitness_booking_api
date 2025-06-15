from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from datetime import datetime
import pytz
import os

tz = pytz.timezone(os.getenv("TIMEZONE"))

def create_class(db: Session, class_data: schemas.FitnessClassCreate):
    class_data.dateTime = class_data.dateTime.astimezone(tz)
    new_class = models.FitnessClass(**class_data.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

def get_all_classes(db: Session):
    return db.query(models.FitnessClass).all()


def create_booking(db: Session, booking: schemas.BookingCreate):
    # Check if email already booked
    existing_booking = db.query(models.Booking).filter(
        models.Booking.client_email == booking.client_email
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="Email already used for booking")

    # Check if class exists
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")

    # Check slot availability
    if fitness_class.availableSlots <= 0:
        raise HTTPException(status_code=400, detail="No slots available")

    fitness_class.availableSlots -= 1
    new_booking = models.Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def get_bookings_by_email(db: Session, email: str):
    return db.query(models.Booking).filter(models.Booking.client_email == email).all()
