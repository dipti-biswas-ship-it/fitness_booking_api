from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class FitnessClassCreate(BaseModel):
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int

class FitnessClassOut(FitnessClassCreate):
    id: int

    class Config:
        from_attributes = True


class FitnessClassUpdate(BaseModel):
    name: Optional[str] = None
    dateTime: Optional[datetime] = None
    instructor: Optional[str] = None
    availableSlots: Optional[int] = None        

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


class BookingUpdate(BaseModel):
    class_id: Optional[int] = None
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None

    class Config:
        from_attributes = True