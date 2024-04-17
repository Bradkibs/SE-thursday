from fastapi import APIRouter, Depends, HTTPException, status
from schema import UserCreate
from db import session
from models import User
from auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/v1")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate = Depends(UserCreate)):
    """Creates a new user in the database."""
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    # Create a new User instance from UserCreate data
    new_user = User(username=user.username, email=user.email, password=hash_password(user.password))

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User Registration success"}



@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Verifies user credentials and returns a success message."""
    username = form_data.username
    password = form_data.password

    user = session.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}