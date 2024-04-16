from pydantic import BaseModel, Field, Optional, EmailStr, UUID4
from datetime import datetime
from uuid import uuid4

class User(BaseModel):
    Id: UUID4 = uuid4()
    username: str
    email: EmailStr = Field(unique=True)
    password: str


class Token(BaseModel):
    Id: UUID4 = uuid4()
    access_token: str
    token_type: str = "bearer"


class Inventory(BaseModel):
    Id: UUID4 = uuid4()
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
