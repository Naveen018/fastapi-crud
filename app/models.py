from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    item_name: str = Field(..., example="Apple")
    quantity: int = Field(..., ge=0, example=10)
    expiry_date: date = Field(..., example="2023-12-31")

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str = Field(..., alias="_id")
    insert_date: datetime

    class Config:
        allow_population_by_field_name = True
        

class ClockInRecordBase(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    location: str = Field(..., example="Office")

class ClockInRecordCreate(ClockInRecordBase):
    pass

class ClockInRecord(ClockInRecordBase):
    id: str = Field(..., alias="_id")
    insert_datetime: datetime

    class Config:
        allow_population_by_field_name = True