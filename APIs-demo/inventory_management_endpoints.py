from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from db import session
from models import Item, User
from schema import Item as ItemSchema
from auth import get_current_user

item_router = APIRouter(prefix="/api/v1")

@item_router.post("/items/", response_model=ItemSchema)
async def create_item(item: ItemSchema, current_user: User = Depends(get_current_user)):
    """Create a new item."""
    db_item = Item(**item.dict(), storekeeper_id=current_user.id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@item_router.get("/items/", response_model=List[ItemSchema])
async def read_items():
    """Get all items."""
    return session.query(Item).all()

@item_router.get("/items/{item_id}", response_model=ItemSchema)
async def read_item(item_id: int):
    """Get a single item by ID."""
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@item_router.put("/items/{item_id}", response_model=ItemSchema)
async def update_item(item_id: int, item: ItemSchema, current_user: User = Depends(get_current_user)):
    """Update an existing item."""
    db_item = session.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if db_item.storekeeper_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this item")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    session.commit()
    session.refresh(db_item)
    return db_item

@item_router.delete("/items/{item_id}", response_model=ItemSchema)
async def delete_item(item_id: int, current_user: User = Depends(get_current_user)):
    """Delete an item."""
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.storekeeper_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this item")
    session.delete(item)
    session.commit()
    return item
