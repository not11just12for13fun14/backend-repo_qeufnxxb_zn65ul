from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Appointment(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=20)
    pet_name: str = Field(..., min_length=1, max_length=100)
    species: str = Field(..., description="dog, cat, rabbit, hamster, guinea pig")
    preferred_date: date
    preferred_time: str = Field(..., description="Preferred time range or slot")
    reason: Optional[str] = Field(None, max_length=500)


class Newsletter(BaseModel):
    email: EmailStr
