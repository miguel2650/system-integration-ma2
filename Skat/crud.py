import models
import schemas
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
    skat_year = db.query(models.SkatYear).last()
    skat_user_year = db.query(models.SkatUserYear).filter(
        models.SkatUserYear.user_id == pay_taxes.user_id and models.SkatUserYear.user_id != skat_year.id)

    amount_due = 0
    user_id = 1  # skat_user_year.user_id
    deposits = requests.get(
        f'localhost:5005/api/list-deposits/{user_id}')
    for item in skat_user_year:
        # If user did not pay taxes past skat years
        # A user is deemed to have paid his taxes if the value is greater than 0
        if(not item.is_paid):
            for deposit in deposits:
                deposit_date = deposit['created_at']
                start_date = item.skat_year.start_date
                end_date = item.skat_year.end_date
                print(start_date)

    req = requests.post(
        "http://localhost:7071/api/Skat_Tax_Calculator", json={"money": pay_taxes.total_amount})
    return "skede"
