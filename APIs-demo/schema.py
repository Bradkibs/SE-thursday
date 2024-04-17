from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, validator


# class UserType(Enum):
#     MANAGER = "Manager"
#     ADMIN = "Admin"
#     STOREKEEPER = "Storekeeper"


class UserBase(BaseModel):
    username: str = Field(..., max_length=255)
    email: EmailStr
    # type: UserType = UserType.STOREKEEPER 


class UserCreate(UserBase):
    password: str = Field(..., min_length=10)
    @validator('password')
    def validate_price(cls, password):
        if len(password) < 10:
            raise ValueError("Password must contain 10 or more alphanumeric characters")
        return password


class UserInDB(UserBase):
    id: int
    password: str

    class Config:
        from_attributes = True


class Item(BaseModel):
    name: str = Field(..., max_length=255)
    price: float = Field(..., ge=1)
    quantity: int = Field(..., ge=1, le=10000)
    description: Optional[str] = Field(..., max_length=1024)

    @validator('quantity')
    def validate_quantity(cls, value):
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

    @validator('price')
    def validate_price(cls, price):
        if price < 1:
            raise ValueError("Price must be at least 1 shilling")
        return price
    
class ItemSchema(Item):
    id: int
    name: str
    price: float
    quantity: int
    description: Optional[str]

    class Config:
        from_attributes = True