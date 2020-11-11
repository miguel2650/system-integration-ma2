from datetime import date
from pydantic import BaseModel, validator
from typing import List


class SkatUser(BaseModel):
    id: int
    user_id: int
    created_at: date
    is_active: bool

    class Config:
        orm_mode = True


class SkatUserYear(BaseModel):
    id: int
    user_id: int
    skat_user_id: int
    skat_year_id: int
    user_id: int
    is_paid: bool
    amount: int

    class Config:
        orm_mode = True


class SkatYear(BaseModel):
    id: int
    label: int
    created_at: date
    modified_at: date
    start_date: date
    end_date: date

    class Config:
        orm_mode = True


class PayTaxes(BaseModel):
    user_id: int
    total_amount: int


class SkatUserCreate(BaseModel):
    user_id: int


class SkatYearCreate(BaseModel):
    label: str
    start_date: date
    end_date: date
