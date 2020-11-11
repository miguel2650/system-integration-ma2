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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs/")

# Get all borgere
@app.get("/api/users", response_model=List[schemas.BorgerUser])
def read_all_borger_users(db: Session = Depends(get_db)):
    return crud.read_all_borger_users(db=db)

# Get a borger
@app.get("/api/user/{userId}", response_model=schemas.BorgerUser)
def read_borger_user(userId: int, db: Session = Depends(get_db)):
    db_borger_user = crud.read_borger_user(db=db, UserId=userId)
    if db_borger_user is None:
        raise HTTPException(status_code=404, detail="BorgerUser not found")
    return db_borger_user


# Create a borger
@app.post("/api/user", response_model=schemas.BorgerUser)
def create_borger_user(borger: schemas.BorgerUserCreate, db: Session = Depends(get_db)):
    return crud.create_borger_user(db=db, borgerUser=borger)

# Update a borger
@app.put("/api/user/{userId}", response_model=schemas.BorgerUser)
def update_borger_user(userId: int, borger: schemas.BorgerUserCreate, db: Session = Depends(get_db)):
    db_borger_user = crud.read_borger_user(db=db, UserId=userId)
    if db_borger_user is None:
        raise HTTPException(status_code=404, detail="BorgerUser not found")
    return crud.update_borger_user(db=db, dbBorgerUser=db_borger_user, borgerUser=borger)

# Deletes a borger
@app.delete("/api/user/{userId}", response_model=bool)
def delete_borger_user(userId: int, db: Session = Depends(get_db)):
    db_borger_user = crud.read_borger_user(db=db, UserId=userId)
    if db_borger_user is None:
        raise HTTPException(status_code=404, detail="BorgerUser not found")
    return crud.delete_borger_user(db=db, borgerUser=db_borger_user)

# Get all address
@app.get("/api/addresses", response_model=List[schemas.Address])
def read_all_borger_address(db: Session = Depends(get_db)):
    return crud.read_all_addresses(db=db)

# Create an address
@app.post("/api/address", response_model=schemas.Address)
def create_borger_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    db_borger_user = crud.read_borger_user(
        db=db, UserId=address.BorgerUserId)
    if db_borger_user is None:
        raise HTTPException(status_code=404, detail="BorgerUser not found")
    return crud.create_address(db=db, address=address)

# Deletes a borger
@app.delete("/api/address/{addressId}", response_model=bool)
def delete_address(addressId: int, db: Session = Depends(get_db)):
    db_address = crud.get_address_by_id(db=db, addressId=addressId)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return crud.delete_address(db=db, address=db_address)
