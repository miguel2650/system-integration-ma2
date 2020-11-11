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


@app.get("/api/skatUsers", response_model=List[schemas.SkatUser])
def read_all_skat_users(db: Session = Depends(get_db)):
    ''' Get all skat users '''
    return crud.read_all_skat_users(db=db)


@app.get("/api/skatUser/{skatUserId}", response_model=schemas.SkatUser)
def read_skat_user(skatUserId: int, db: Session = Depends(get_db)):
    ''' Get skat user by id '''
    db_skat_user = crud.read_skat_user(db=db, user_id=skatUserId)
    if db_skat_user is None:
        raise HTTPException(status_code=404, detail="skat user not found")
    return db_skat_user


@app.post("/api/skatUser", response_model=schemas.SkatUser)
def create_skat_user(skat_user: schemas.SkatUserCreate, db: Session = Depends(get_db)):
    ''' Create new skat user '''
    return crud.create_skat_user(db=db, skat_user=skat_user)


@app.put("/api/skatUser/{skatUserId}", response_model=schemas.SkatUser)
def update_skat_user(skatUserId: int, skat_user: schemas.SkatUserCreate, db: Session = Depends(get_db)):
    ''' Update existing skat user '''
    db_skat_user = crud.read_skat_user(db=db, user_id=skatUserId)
    if db_skat_user is None:
        raise HTTPException(status_code=404, detail="Skat user not found")
    return crud.update_skat_user(db=db, db_skat_user=db_skat_user, skat_user=skat_user)


@app.delete("/api/skatUser/{skatUserId}", response_model=bool)
def delete_skat_user(skatUserId: int, db: Session = Depends(get_db)):
    ''' Delete skat user by id '''
    db_skat_user = crud.read_skat_user(db=db, user_id=skatUserId)
    if db_skat_user is None:
        raise HTTPException(status_code=404, detail="Skat user not found")
    return crud.delete_skat_user(db=db, skat_user=db_skat_user)


@app.get("/api/skatYears", response_model=List[schemas.SkatYear])
def read_all_skatYears(db: Session = Depends(get_db)):
    ''' Get all skatYears '''
    return crud.read_all_skatYears(db=db)


@app.get("/api/skatYear/{skatUserId}", response_model=schemas.SkatYear)
def read_skatYear(skatUserId: int, db: Session = Depends(get_db)):
    ''' Get skatYear by skat user id '''
    db_skatYear = crud.read_skatYear(db=db, skat_user_id=skatUserId)
    if db_skatYear is None:
        raise HTTPException(status_code=404, detail="SkatYear not found")
    return db_skatYear


@app.post("/api/skatYear", response_model=schemas.SkatYear)
def create_skatYear(skatYear: schemas.SkatYearCreate, db: Session = Depends(get_db)):
    ''' Create new skatYear '''
    db_skat_user = crud.read_skat_user(
        db=db, user_id=skatYear.skat_user_id)
    if db_skat_user is None:
        raise HTTPException(status_code=404, detail="SkatYear not found")
    return crud.create_skatYear(db=db, skatYear=skatYear)


@app.delete("/api/skatYear/{skatUserId}", response_model=bool)
def delete_skatYear(skatUserId: int, db: Session = Depends(get_db)):
    ''' Delete skatYear by skat user id '''
    db_skatYear = crud.read_skatYear(db=db, skat_user_id=skatUserId)
    if db_skatYear is None:
        raise HTTPException(status_code=404, detail="SkatYear not found")
    return crud.delete_skatYear(db=db, skatYear=db_skatYear)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5005)