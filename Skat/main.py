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


@app.get("/api/user-management/users", response_model=List[schemas.SkatUser])
def read_all_skat_users(db: Session = Depends(get_db)):
    ''' Get all skat users '''
    return crud.read_all_skat_users(db=db)


@app.get("/api/user-management/users/{skatUserId}", response_model=schemas.SkatUser)
def read_skat_user(skatUserId: int, db: Session = Depends(get_db)):
    ''' Get skat user by id '''
    db_skat_user = crud.read_skat_user(db=db, user_id=skatUserId)
    if db_skat_user is None:
        raise HTTPException(status_code=404, detail="skat user not found")
    return db_skat_user


@app.post("/api/user-management/users", response_model=schemas.SkatUser)
def create_skat_user(skat_user: schemas.SkatUserCreate, db: Session = Depends(get_db)):
    ''' Create new skat user '''
    return crud.create_skat_user(db=db, skat_user=skat_user)


@app.put("/api/user-management/users/{skatUserId}", response_model=schemas.SkatUser)
def update_skat_user(skatUserId: int, skat_user: schemas.SkatUserCreate, db: Session = Depends(get_db)):
    ''' Update existing skat user '''
    db_skat_user = crud.read_skat_user(db=db, user_id=skatUserId)
    if db_skat_user is None:
        raise HTTPException(status_code=404, detail="Skat user not found")
    return crud.update_skat_user(db=db, db_skat_user=db_skat_user, skat_user=skat_user)


@app.delete("/api/user-management/users/{skatUserId}", response_model=bool)
def delete_skat_user(skatUserId: int, db: Session = Depends(get_db)):
    ''' Delete skat user by id '''
    db_skat_user = crud.read_skat_user(db=db, user_id=skatUserId)
    if db_skat_user is None:
        raise HTTPException(status_code=404, detail="Skat user not found")
    return crud.delete_skat_user(db=db, skat_user=db_skat_user)


@app.get("/api/year-management/years", response_model=List[schemas.SkatYear])
def read_all_skat_years(db: Session = Depends(get_db)):
    ''' Get all skatYears '''
    return crud.read_all_skat_years(db=db)


@app.get("/api/year-management/years/{skatYearId}", response_model=schemas.SkatYear)
def read_skat_year(skatYearId: int, db: Session = Depends(get_db)):
    ''' Get SkatYear by skat year id '''
    db_skat_year = crud.read_skat_year(db=db, skat_year_id=skatYearId)
    if db_skat_year is None:
        raise HTTPException(status_code=404, detail="SkatYear not found")
    return db_skat_year


@app.post("/api/year-management/years", response_model=schemas.SkatYear)
def create_skat_year(skatYear: schemas.SkatYearCreate, db: Session = Depends(get_db)):
    ''' Create new skatYear '''
    return crud.create_skat_year(db=db, skat_year=skatYear)


@app.delete("/api/year-management/years/{skatYearId}", response_model=bool)
def delete_skat_year(skatYearId: int, db: Session = Depends(get_db)):
    ''' Delete skatYear by skat user id '''
    db_skat_year = crud.read_skat_year(db=db, skat_year_id=skatYearId)
    if db_skat_year is None:
        raise HTTPException(status_code=404, detail="SkatYear not found")
    return crud.delete_skat_year(db=db, skat_year=db_skat_year)


@app.put("/api/year-management/years/{skatYearId}", response_model=schemas.SkatYear)
def update_skat_user(skatYearId: int, skat_year: schemas.SkatYearCreate, db: Session = Depends(get_db)):
    ''' Update existing skat year '''
    db_skat_year = crud.read_skat_year(db=db, user_id=skatYearId)
    if db_skat_year is None:
        raise HTTPException(status_code=404, detail="Skat year not found")
    return crud.update_skat_year(db=db, db_skat_year=db_skat_year, skat_year=skat_year)


@app.post("/api/tax-management/pay-taxes", response_model=List[schemas.SkatUserYear])
def pay_taxes(pay_taxes: schemas.PayTaxes, db: Session = Depends(get_db)):
    try:
        skat_user_years = crud.pay_taxes(db=db, pay_taxes=pay_taxes)
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="Failed paying taxes")
    return skat_user_years


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", reload=True, port=5006)
