from middlewares.auth_middleware import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token, decode_access_token
from config.database import db

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register")
async def register(user: User):
    if await db["users"].find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(user.password)
    await db["users"].insert_one({"username": user.username, "password": hashed_password})
    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login(user: User):
    db_user = await db["users"].find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}
