from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models, database, crud

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

### CLASSES
@router.post("/classes", response_model=schemas.FitnessClassOut)
def create_class(class_data: schemas.FitnessClassCreate, db: Session = Depends(get_db)):
    return crud.create_class(db, class_data)

@router.get("/classes", response_model=list[schemas.FitnessClassOut])
def get_classes(db: Session = Depends(get_db)):
    return crud.get_all_classes(db)

@router.patch("/classes/{class_id}", response_model=schemas.FitnessClassOut)
def update_class(class_id: int, updates: schemas.FitnessClassUpdate, db: Session = Depends(get_db)):
    return crud.update_class(db, class_id, updates)

@router.put("/classes/{class_id}", response_model=schemas.FitnessClassOut)
def put_class(class_id: int, updates: schemas.FitnessClassUpdate, db: Session = Depends(get_db)):
    return crud.update_class(db, class_id, updates)

@router.delete("/classes/{class_id}", status_code=204)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(fitness_class)
    db.commit()
    return {"detail": "Class deleted"}


### BOOKINGS
@router.post("/book", response_model=schemas.BookingOut)
def create_booking(data: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, data)

@router.get("/bookings", response_model=list[schemas.BookingOut])
def get_bookings(email: str = None, db: Session = Depends(get_db)):
    if email:
        return crud.get_bookings_by_email(db, email)
    return crud.get_all_bookings(db)


### Update Routes
@router.put("/bookings/{booking_id}", response_model=schemas.BookingOut)

@router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
def update_booking(
    booking_id: int,
    booking_data: schemas.BookingUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_booking(db, booking_id, booking_data)


@router.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"detail": "Booking deleted"}
