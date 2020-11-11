from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, Boolean
from database import Base
import datetime


class BorgerUser(Base):
    __tablename__ = 'BorgerUser'
    id = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer)
    CreatedAt = Column(Date, default=datetime.datetime.utcnow)


class Address(Base):
    __tablename__ = 'Address'

    id = Column(Integer, primary_key=True, index=True)
    BorgerUserId = Column(Integer, ForeignKey(
        'BorgerUser.UserId'))
    CreatedAt = Column(Date, default=datetime.datetime.utcnow)
    IsValid = Column(Boolean, default=True)
