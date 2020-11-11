from datetime import date
from pydantic import BaseModel, validator
from typing import List


class BankUser(BaseModel):
    id: int
    user_id: int
    created_at: date
    modified_at: date

    class Config:
        orm_mode = True


class BankUserCreate(BaseModel):
    user_id: int


class Account(BaseModel):
    id: int
    bank_user_id: int
    account_no: int
    is_student: bool
    created_at: date
    modified_at: date
    interest_rate: int
    amount: int

    class Config:
        orm_mode = True


class AccountCreate(BaseModel):
    bank_user_id: int
    account_no: int
    is_student: bool
    interest_rate: int
    amount: int


class Loan(BaseModel):
    id: int
    user_id: int
    created_at: date
    modified_at: date
    amount: int

    class Config:
        orm_mode = True


class Deposit(BaseModel):
    id: int
    bank_user_id: int
    created_at: date
    amount: int

    class Config:
        orm_mode = True


class BankUserDeposit(BaseModel):
    bank_user_id: int
    amount: int

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Amount must be positive')
        return v


class LoanCreate(BaseModel):
    user_id: int
    amount: int


class PayLoan(BaseModel):
    user_id: int
    loan_id: int


class WithdrawMoney(BaseModel):
    user_id: int
    amount: int
