from pydantic import BaseModel, EmailStr
from datetime import datetime

class FitnessClassCreate(BaseModel):
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int

class FitnessClassOut(FitnessClassCreate):
    id: int
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingOut(BookingCreate):
    id: int
    class Config:
        from_attributes = True
