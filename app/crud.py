from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from datetime import datetime
import pytz
import os

tz = pytz.timezone(os.getenv("TIMEZONE"))

# Create class
def create_class(db: Session, class_data: schemas.FitnessClassCreate):
    class_data.dateTime = class_data.dateTime.astimezone(tz)
    new_class = models.FitnessClass(**class_data.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

def get_all_classes(db: Session):
    return db.query(models.FitnessClass).all()

### Update Class
def update_class(db: Session, class_id: int, updates: schemas.FitnessClassUpdate):
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")

    update_data = updates.dict(exclude_unset=True)

    if "dateTime" in update_data and update_data["dateTime"]:
        update_data["dateTime"] = update_data["dateTime"].astimezone(tz)

    for key, value in update_data.items():
        setattr(fitness_class, key, value)

    db.commit()
    db.refresh(fitness_class)
    return fitness_class


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

def get_all_bookings(db: Session):  
    return db.query(models.Booking).all()

### Update Booking
def update_booking(db: Session, booking_id: int, booking_data: schemas.BookingUpdate):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking_data.client_email:
        existing = db.query(models.Booking).filter(
            models.Booking.client_email == booking_data.client_email,
            models.Booking.id != booking_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already used for another booking")

    for field, value in booking_data.dict(exclude_unset=True).items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)
    return booking
