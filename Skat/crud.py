import models
import schemas
import datetime
from sqlalchemy.orm import Session
import requests


def create_skat_user(db: Session, skat_user: schemas.SkatUser):
    ''' '''
    db_skat_user = models.SkatUser(user_id=skat_user.user_id)
    db.add(db_skat_user)
    db.commit()
    db.refresh(db_skat_user)
    return db_skat_user


def read_skat_user(db: Session, user_id: int):
    ''' '''
    return db.query(models.SkatUser).filter(models.SkatUser.user_id == user_id).first()


def read_all_skat_users(db: Session):
    ''' '''
    return db.query(models.SkatUser).all()


def update_skat_user(db: Session, db_skat_user: schemas.SkatUser, skat_user: schemas.SkatUser):
    ''' '''
    db_skat_user.user_id = skat_user.user_id
    db.commit()
    return db_skat_user


def delete_skat_user(db: Session, skat_user: schemas.SkatUser):
    db_skat_user_deleted = db.query(models.SkatUser).filter(
        models.SkatUser.user_id == skat_user.user_id).delete()
    db.commit()
    return db_skat_user_deleted


def create_skat_year(db: Session, skat_year: schemas.SkatYear):
    ''' '''
    db_skat_year = models.SkatYear(
        label=skat_year.label, start_date=skat_year.start_date, end_date=skat_year.end_date)
    db.add(db_skat_year)
    db.commit()
    db.refresh(db_skat_year)
    db_skat_user_years = db.query(models.SkatUser).all()
    for skat_user in db_skat_user_years:
        skat_user_year = models.SkatUserYear(
            skat_user_id=skat_user.id,
            skat_year_id=db_skat_year.id,
            user_id=skat_user.user_id,
        )
        db.add(skat_user_year)
    db.commit()
    return db_skat_year


def read_skat_year(db: Session, skat_year_id: int):
    ''' '''
    return db.query(models.SkatYear).filter(models.SkatYear.id == skat_year_id).first()


def read_all_skat_years(db: Session):
    ''' '''
    return db.query(models.SkatYear).all()


def update_skat_year(db: Session, db_skat_year: schemas.SkatYear, skat_year: schemas.SkatYearCreate):
    db_skat_year.label = skat_year.label
    db_skat_year.start_date = skat_year.start_date
    db_skat_year.end_date = skat_year.end_date
    db.commit()
    return db_skat_year


def delete_skat_year(db: Session, skat_year: schemas.SkatYear):
    ''' '''
    db_skat_year_delete = db.query(models.SkatYear).filter(
        models.SkatYear.id == skat_year.id).delete()
    db_skat_user_year_delete = db.query(models.SkatUserYear).filter(
        models.SkatUserYear.skat_year_id == skat_year.id).delete()
    db.commit()
    return db_skat_year_delete and db_skat_user_year_delete


def pay_taxes(db: Session, pay_taxes: schemas.PayTaxes):
    # /api/account/{bankUserId}
    skat_year = db.query(models.SkatYear).first()
    skat_user_years = db.query(models.SkatUserYear).filter(
        models.SkatUserYear.user_id == pay_taxes.user_id and models.SkatUserYear.user_id != skat_year.id)

    amount_due = 0
    user_id = pay_taxes.user_id
    deposits = requests.get(
        f'http://localhost:5005/api/list-deposits/{user_id}')
    for skat_user_year in skat_user_years:
        # If user did not pay taxes past skat years
        # A user is deemed to have paid his taxes if the value is greater than 0
        if(not skat_user_year.is_paid):
            for deposit in deposits.json():
                deposit_date = datetime.datetime.strptime(
                    deposit['created_at'], "%Y-%m-%d").date()
                start_date = skat_user_year.skat_year.start_date
                end_date = skat_user_year.skat_year.end_date
                if deposit_date >= start_date and deposit_date <= end_date:
                    amount_due += int(deposit['amount'])
                    skat_user_year.is_paid = True
    # If the user has a sufficient amount of money in their bank account
    # The missing amount of taxes will be withdrawn.

    req = requests.post(
        "http://localhost:7071/api/Skat_Tax_Calculator", json={"money": amount_due})
    req.raise_for_status()
    tax_amount = req.json()['tax_money']
    req = requests.post(
        "http://localhost:5005/api/withdraw-money",
        json={
            "user_id": user_id,
            "amount": tax_amount
        }
    )
    req.raise_for_status()
    db.commit()

    return skat_user_years
