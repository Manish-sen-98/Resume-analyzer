from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from schemas.auth import SignupRequest, LoginRequest, UserResponse
from db.database import auth_collection
from core.security import hash_password, verify_password, create_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: SignupRequest):
    
    existing_user = await auth_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
   
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
   
    result = await auth_collection.insert_one(user_data)
    
    return UserResponse(
        id=str(result.inserted_id),
        username=user.username,
        email=user.email
    )

@router.post("/login")
async def login(credentials: LoginRequest):
    
    user = await auth_collection.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_token(
        username= user['username']
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

