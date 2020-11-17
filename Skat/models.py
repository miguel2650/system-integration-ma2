from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, Boolean
from database import Base
import datetime


class SkatUser(Base):
    __tablename__ = 'SkatUser'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column('UserId', Integer)
    created_at = Column('CreatedAt', Date, default=datetime.datetime.utcnow)
    is_active = Column('IsActive', Boolean, default=True)
    skat_year = relationship('SkatUserYear')


class SkatUserYear(Base):
    __tablename__ = 'SkatUserYear'
    id = Column('id', Integer, primary_key=True, index=True)
    skat_user_id = Column('SkatUserId', Integer, ForeignKey(
        'SkatUser.id', ondelete='CASCADE'))
    skat_year_id = Column('SkatYearId', Integer, ForeignKey(
        'SkatYear.id', ondelete='CASCADE'))
    user_id = Column('UserId', Integer)
    is_paid = Column('IsPaid', Boolean, default=False)
    amount = Column('Amount', Integer)
    skat_year = relationship('SkatYear')


class SkatYear(Base):
    __tablename__ = 'SkatYear'
    id = Column(Integer, primary_key=True, index=True)
    label = Column('Label', String)
    created_at = Column('CreatedAt', Date, default=datetime.datetime.utcnow)
    modified_at = Column('ModifiedAt', Date, default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)
    start_date = Column('StartDate', Date)
    end_date = Column('EndDate', Date)
