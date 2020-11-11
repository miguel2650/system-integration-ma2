import models
import schemas
from sqlalchemy.orm import Session


def create_borger_user(db: Session, borgerUser: schemas.BorgerUserCreate):
    ''' Creates a new borger in the BorgerUser table. Takes UserId as only parameter. Id and CreatedAt will be provided by system. '''
    db_borger_user = models.BorgerUser(UserId=borgerUser.UserId)
    db.add(db_borger_user)
    db.commit()
    db.refresh(db_borger_user)
    return db_borger_user


def read_borger_user(db: Session, UserId: int):
    ''' Returns one single borger from BorgerUser table and the borgers active address from Address table where UserId matches. Takes UserId as only parameter. '''
    return db.query(models.BorgerUser).filter(models.BorgerUser.UserId == UserId).first()


def read_all_borger_users(db: Session):
    '''  Returns all borgere from BorgerUser table '''
    return db.query(models.BorgerUser).all()


def update_borger_user(db: Session, dbBorgerUser: schemas.BorgerUser, borgerUser: schemas.BorgerUser):
    dbBorgerUser.UserId = borgerUser.UserId
    db.commit()
    return dbBorgerUser


def delete_borger_user(db: Session, borgerUser: schemas.BorgerUser):
    address_deleted = db.query(models.Address).filter(
        models.Address.BorgerUserId == borgerUser.UserId).delete()
    user_deleted = db.query(models.BorgerUser).filter(
        models.BorgerUser.id == borgerUser.id).delete()
    db.commit()
    return user_deleted


def create_address(db: Session, address: schemas.AddressCreate):
    ''' Creates a new address in the Address table if the BorgerUserId matches a UserId in the BorgerUser table. '''
    ''' New address IsValid=True by default - therefore all other addresses is set to IsValid=False. Only 1 address may be Valid '''
    db.query(models.Address).filter(models.Address.BorgerUserId ==
                                    address.BorgerUserId).update({'IsValid': False})
    db_borger_address = models.Address(
        BorgerUserId=address.BorgerUserId)
    db.add(db_borger_address)
    db.commit()
    db.refresh(db_borger_address)
    return db_borger_address


def read_address(db: Session, UserId: int):
    return db.query(models.BorgerUser).filter(models.BorgerUser.UserId == UserId and models.Address.IsValid)


def read_all_addresses(db: Session):
    return db.query(models.Address).all()


def delete_address(db: Session, address: schemas.Address):
    address_deleted = db.query(models.Address).filter(
        models.Address.id == address.id).delete()
    db.commit()
    return address_deleted


def get_address_by_id(db: Session, addressId: int):
    return db.query(models.Address).get(addressId)
