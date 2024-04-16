from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import Config
from .models import User, Inventory
from datetime import datetime
from sqlalchemy.sql.expression import and_

DATABASE_URL = Config.POSTGRES_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)



def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Inventory CRUD functions (Create, Read, Update, Delete)
def create_inventory(db: Session, inventory: Inventory):
    db.add(inventory)
    db.commit()
    db.refresh(inventory)  # Refresh to get generated ID
    return inventory

def get_inventories(db: Session, 
                    start_date: datetime | None = None, 
                    end_date: datetime | None = None, 
                    item_name: str | None = None, 
                    min_price: float | None = None, 
                    max_price: float | None = None):
    query = db.query(Inventory)
    filters = []
    if start_date and end_date:
        filters.append(Inventory.created_at >= start_date)
        filters.append(Inventory.created_at <= end_date)
    if item_name:
        filters.append(Inventory.name.ilike(f"%{item_name}%"))  # Case-insensitive search
    if min_price and max_price:
        filters.append(and_(Inventory.price >= min_price, Inventory.price <= max_price))
    elif min_price:
        filters.append(Inventory.price >= min_price)
    elif max_price:
        filters.append(Inventory.price <= max_price)
    if filters:
        query = query.filter(*filters)  # Apply all filters

    return query.all()

def get_inventory_by_id(db: Session, inventory_id: int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()

def update_inventory(db: Session, inventory_id: int, inventory_data: Inventory):
    inventory = get_inventory_by_id(db, inventory_id)
    if inventory:
        for field, value in inventory_data.model_dump(exclude_unset=True).items():
            setattr(inventory, field, value)
        db.commit()
        db.refresh(inventory)
        return inventory
    return None

def delete_inventory(db: Session, inventory_id: int):
    inventory = get_inventory_by_id(db, inventory_id)
    return inventory
