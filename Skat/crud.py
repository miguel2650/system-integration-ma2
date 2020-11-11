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
    db_skat_skat_year = models.skatYear(skat_user_id=skat_year.skat_user_id, skat_year_no=skat_year.skat_year_no,
                                        is_student=skat_year.is_student, interest_rate=skat_year.interest_rate, amount=skat_year.amount)
    db.add(db_skat_skat_year)
    db.commit()
    db.refresh(db_skat_skat_year)
    return db_skat_skat_year


def read_skat_year(db: Session, skat_user_id: int):
    ''' '''
    return db.query(models.skatYear).filter(models.skatYear.skat_user_id == skat_user_id).first()


def read_all_skat_years(db: Session):
    ''' '''
    return db.query(models.skatYear).all()


def update_skat_year(db: Session, db_skat_year: schemas.SkatYear, skat_year: schemas.SkatYear):
    db_skat_year.skat_user_id = skat_year.skat_user_id
    db_skat_year.skat_year_no = skat_year.skat_year_no
    db_skat_year.is_student = skat_year.is_student
    db_skat_year.interest_rate = skat_year.interest_rate
    db_skat_year.amount = skat_year.amount
    db.commit()
    return db_skat_year


def delete_skat_year(db: Session, skat_year: schemas.SkatYear):
    ''' '''
    db_skat_year_delete = db.query(models.skatYear).filter(
        models.skatYear.skat_user_id == skat_year.skat_user_id).delete()
    db.commit()
    return db_skat_year_delete


def pay_taxes(db: Session, pay_taxes: schemas.PayTaxes):
    # /api/account/{bankUserId}
    skat_year = db.query(models.SkatYear).last()
    skat_user_year = db.query(models.SkatUserYear).filter(
        models.SkatUserYear.user_id == pay_taxes.user_id and models.SkatUserYear.user_id != skat_year.id)

    for item in skat_user_year:
        # If user did not pay taxes past skat years
        # A user is deemed to have paid his taxes if the value is greater than 0
        if(not item.is_paid and item.amount > 0):

            return None

    req = requests.post(
        "http://localhost:7071/api/Skat_Tax_Calculator", json={"money": pay_taxes.total_amount})
    return "skede"
