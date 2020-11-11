from datetime import date
from pydantic import BaseModel
from typing import List


class BorgerUser(BaseModel):
    id: int
    UserId: int
    CreatedAt: date

    class Config:
        orm_mode = True


class BorgerUserCreate(BaseModel):
    UserId: int


class AddressCreate(BaseModel):
    BorgerUserId: int


class Address(BaseModel):
    id: int
    BorgerUserId: int
    CreatedAt: date
    IsValid: bool

    class Config:
        orm_mode = True
