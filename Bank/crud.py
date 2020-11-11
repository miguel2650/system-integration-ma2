import models
import schemas
from sqlalchemy.orm import Session
import requests


def create_bank_user(db: Session, bank_user: schemas.BankUser):
    ''' '''
    db_bank_user = models.BankUser(user_id=bank_user.user_id)
    db.add(db_bank_user)
    db.commit()
    db.refresh(db_bank_user)
    return db_bank_user


def read_bank_user(db: Session, user_id: int):
    ''' '''
    return db.query(models.BankUser).filter(models.BankUser.user_id == user_id).first()


def read_all_bank_users(db: Session):
    ''' '''
    return db.query(models.BankUser).all()


def update_bank_user(db: Session, db_bank_user: schemas.BankUser, bank_user: schemas.BankUser):
    ''' '''
    db_bank_user.user_id = bank_user.user_id
    db.commit()
    return db_bank_user


def delete_bank_user(db: Session, bank_user: schemas.BankUser):
    ''' Deleting bank user and associated account is deleted like this 
    as cascade will not work in the database when using filter '''
    db_account_deleted = db.query(models.Account).filter(
        models.Account.bank_user_id == bank_user.user_id).delete()
    db_bank_user_deleted = db.query(models.BankUser).filter(
        models.BankUser.user_id == bank_user.user_id).delete()
    db.commit()
    return db_bank_user_deleted


def create_account(db: Session, account: schemas.Account):
    ''' '''
    db_bank_account = models.Account(bank_user_id=account.bank_user_id, account_no=account.account_no,
                                     is_student=account.is_student, interest_rate=account.interest_rate, amount=account.amount)
    db.add(db_bank_account)
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account


def read_account(db: Session, bank_user_id: int):
    ''' '''
    return db.query(models.Account).filter(models.Account.bank_user_id == bank_user_id).first()


def read_all_accounts(db: Session):
    ''' '''
    return db.query(models.Account).all()


def update_account(db: Session, db_account: schemas.Account, account: schemas.Account):
    db_account.bank_user_id = account.bank_user_id
    db_account.account_no = account.account_no
    db_account.is_student = account.is_student
    db_account.interest_rate = account.interest_rate
    db_account.amount = account.amount
    db.commit()
    return db_account


def delete_account(db: Session, account: schemas.Account):
    ''' '''
    db_account_delete = db.query(models.Account).filter(
        models.Account.bank_user_id == account.bank_user_id).delete()
    db.commit()
    return db_account_delete


def add_deposit(db: Session, bank_user_deposit: schemas.BankUserDeposit):
    req = requests.post("http://localhost:7071/api/Interest_Rate_Function",
                        json={"amount": bank_user_deposit.amount})
    calculated_amount = int(req.json()['amount'])
    db_deposit = models.Deposit(
        bank_user_id=bank_user_deposit.bank_user_id,
        amount=calculated_amount
    )
    account = read_account(
        db=db,
        bank_user_id=bank_user_deposit.bank_user_id
    )
    account.amount += calculated_amount
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit


def read_all_deposits(db: Session, bank_user_id: int):
    ''' '''
    return db.query(models.Deposit).filter(models.Deposit.bank_user_id == bank_user_id).all()


def create_loan(db: Session, bank_user: schemas.BankUser, loan_amount: int):
    ''' '''
    account = read_account(db=db, bank_user_id=bank_user.user_id)
    req = requests.post("http://localhost:7071/api/Loan_Algorithm_Function",
                        json={"loan_amount": loan_amount, "total_amount": account.amount})
    req.raise_for_status()
    db_loan = models.Loan(
        user_id=bank_user.user_id,
        amount=loan_amount
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def pay_loan(db: Session, bank_user: schemas.BankUser, loan_id: int):
    ''' '''
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    db_account = read_account(db=db, bank_user_id=bank_user.user_id)
    if(db_loan.amount > db_account.amount):
        raise ValueError
    else:
        db_loan.amount = 0
        db.commit()
    return db_loan


def read_all_loans(db: Session, bank_user_id: int):
    ''' '''
    return db.query(models.Loan).filter(models.Loan.user_id == bank_user_id and models.Loan.amount > 0).all()


def withdraw_money(db: Session, bank_user: schemas.BankUser, amount: int):
    ''' '''
    db_account = read_account(db=db, bank_user_id=bank_user.user_id)
    if (amount > db_account.amount):
        raise ValueError
    else:
        db_account.amount -= amount
    return db_account
