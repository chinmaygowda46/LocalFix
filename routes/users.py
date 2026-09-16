from fastapi import APIRouter, HTTPException
from database import users_collection
from pydantic import BaseModel
import bcrypt
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user: UserRegister):

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    )

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password.decode("utf-8")
    }

    result = users_collection.insert_one(
        user_data
    )

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


@router.post("/login")
def login(user: UserLogin):

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_match = bcrypt.checkpw(
        user.password.encode("utf-8"),
        existing_user["password"].encode("utf-8")
    )

    if not password_match:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = jwt.encode(
        {
            "user_id": str(existing_user["_id"]),
            "email": existing_user["email"]
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }