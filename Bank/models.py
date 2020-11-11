from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, Boolean
from database import Base
import datetime


class BankUser(Base):
    __tablename__ = 'BankUser'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column('UserId', Integer)
    created_at = Column('CreatedAt', Date, default=datetime.datetime.utcnow)
    modified_at = Column('ModifiedAt', Date, default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)
    account = relationship("Account", backref="parent", passive_deletes=True)


class Account(Base):
    __tablename__ = 'Account'
    id = Column('id', Integer, primary_key=True, index=True)
    bank_user_id = Column('BankUserId', Integer, ForeignKey(
        'BankUser.UserId', ondelete='CASCADE'))
    account_no = Column('AccountNo', Integer)
    is_student = Column('isStudent', Boolean)
    created_at = Column('CreatedAt', Date, default=datetime.datetime.utcnow)
    modified_at = Column('ModifiedAt', Date, default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)
    interest_rate = Column('IntrestRate', Integer)
    amount = Column('Amount', Integer)


class Loan(Base):
    __tablename__ = 'Loan'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column('UserId', Integer)
    created_at = Column('CreatedAt', Date, default=datetime.datetime.utcnow)
    modified_at = Column('ModifiedAt', Date, default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)
    amount = Column('Amount', Integer)


class Deposit(Base):
    __tablename__ = 'Deposit'
    id = Column('id', Integer, primary_key=True, index=True)
    bank_user_id = Column('BankUserId', Integer, ForeignKey(
        'BankUser.UserId', ondelete='CASCADE'))
    created_at = Column('CreatedAt', Date, default=datetime.datetime.utcnow)
    amount = Column('Amount', Integer)
