import uvicorn
from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi import Depends, FastAPI, HTTPException

import models
import schemas
import crud
from database import SessionLocal, engine
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WoooooooooooW!",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    ''' Return swagger documentation '''
    return RedirectResponse(url="/docs/")


@app.get("/api/bankUsers", response_model=List[schemas.BankUser])
def read_all_bank_users(db: Session = Depends(get_db)):
    ''' Get all bank users '''
    return crud.read_all_bank_users(db=db)


@app.get("/api/bankUser/{bankUserId}", response_model=schemas.BankUser)
def read_bank_user(bankUserId: int, db: Session = Depends(get_db)):
    ''' Get bank user by id '''
    db_bank_user = crud.read_bank_user(db=db, user_id=bankUserId)
    if db_bank_user is None:
        raise HTTPException(status_code=404, detail="bank user not found")
    return db_bank_user


@app.post("/api/bankUser", response_model=schemas.BankUser)
def create_bank_user(bank_user: schemas.BankUserCreate, db: Session = Depends(get_db)):
    ''' Create new bank user '''
    return crud.create_bank_user(db=db, bank_user=bank_user)


@app.put("/api/bankUser/{bankUserId}", response_model=schemas.BankUser)
def update_bank_user(bankUserId: int, bank_user: schemas.BankUserCreate, db: Session = Depends(get_db)):
    ''' Update existing bank user '''
    db_bank_user = crud.read_bank_user(db=db, user_id=bankUserId)
    if db_bank_user is None:
        raise HTTPException(status_code=404, detail="Bank user not found")
    return crud.update_bank_user(db=db, db_bank_user=db_bank_user, bank_user=bank_user)


@app.delete("/api/bankUser/{bankUserId}", response_model=bool)
def delete_bank_user(bankUserId: int, db: Session = Depends(get_db)):
    ''' Delete bank user by id '''
    db_bank_user = crud.read_bank_user(db=db, user_id=bankUserId)
    if db_bank_user is None:
        raise HTTPException(status_code=404, detail="Bank user not found")
    return crud.delete_bank_user(db=db, bank_user=db_bank_user)


@app.get("/api/accounts", response_model=List[schemas.Account])
def read_all_accounts(db: Session = Depends(get_db)):
    ''' Get all accounts '''
    return crud.read_all_accounts(db=db)


@app.get("/api/account/{bankUserId}", response_model=schemas.Account)
def read_account(bankUserId: int, db: Session = Depends(get_db)):
    ''' Get account by bank user id '''
    db_account = crud.read_account(db=db, bank_user_id=bankUserId)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.post("/api/account", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    ''' Create new account '''
    db_bank_user = crud.read_bank_user(
        db=db, user_id=account.bank_user_id)
    if db_bank_user is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return crud.create_account(db=db, account=account)


@app.delete("/api/account/{bankUserId}", response_model=bool)
def delete_account(bankUserId: int, db: Session = Depends(get_db)):
    ''' Delete account by bank user id '''
    db_account = crud.read_account(db=db, bank_user_id=bankUserId)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return crud.delete_account(db=db, account=db_account)


@app.post("/api/add-deposit", response_model=schemas.Deposit)
def add_deposit(bank_user_deposit: schemas.BankUserDeposit, db: Session = Depends(get_db)):
    ''' Takes "amount" and "bank_user_id" as parameters. Must not be null or negative. The interest rate will be saved in the Deposits table in the database. '''
    db_deposit = crud.add_deposit(db=db, bank_user_deposit=bank_user_deposit)
    return db_deposit


@app.get("/api/list-deposits/{bankUserId}", response_model=List[schemas.Deposit])
def read_all_deposits(bankUserId: int, db: Session = Depends(get_db)):
    db_deposits = crud.read_all_deposits(db=db, bank_user_id=bankUserId)
    if len(db_deposits) <= 0:
        raise HTTPException(status_code=404, detail="Deposits not found")
    return db_deposits


@app.post("/api/create-loan", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    ''' '''
    db_bank_user = crud.read_bank_user(db=db, user_id=loan.user_id)
    if db_bank_user is None:
        raise HTTPException(status_code=404, detail="Bank user not found")
    try:
        loan = crud.create_loan(
            db=db, bank_user=db_bank_user, loan_amount=loan.amount)
    except requests.exceptions.HTTPError as error:
        raise HTTPException(status_code=404, detail=str(error))
    return loan


@app.post("/api/pay-loan", response_model=schemas.Loan)
def pay_loan(loan: schemas.PayLoan, db: Session = Depends(get_db)):
    ''' '''
    db_bank_user = crud.read_bank_user(db=db, user_id=loan.user_id)
    if db_bank_user is None:
        raise HTTPException(status_code=404, detail="Bank user not found")
    try:
        loan = crud.pay_loan(db=db, bank_user=db_bank_user,
                             loan_id=loan.loan_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    return loan


@app.get("/api/list-loans/{bankUserId}", response_model=List[schemas.Loan])
def read_all_loans(bankUserId: int, db: Session = Depends(get_db)):
    ''' '''
    db_loans = crud.read_all_loans(db=db, bank_user_id=bankUserId)
    if len(db_loans) <= 0:
        raise HTTPException(status_code=404, detail="No loans")
    return db_loans


@app.post("/api/withdraw-money", response_model=schemas.Account)
def withdraw_money(withdraw: schemas.WithdrawMoney, db: Session = Depends(get_db)):
    ''' '''
    db_bank_user = crud.read_bank_user(db=db, user_id=withdraw.user_id)
    if db_bank_user is None:
        raise HTTPException(status_code=404, detail="Bank user not found")
    try:
        withdraw = crud.withdraw_money(
            db=db, bank_user=db_bank_user, amount=withdraw.amount)
    except ValueError as error:
        raise HTTPException(status_code=404, detail='Insufficient funds')
    return withdraw


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, host="0.0.0.0", port=5005)
