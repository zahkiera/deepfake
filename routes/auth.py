from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from db import add_user, authenticate_user

router = APIRouter()

# Request schemas --
class RegisterRequest(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=10)
    firstName: str
    lastName: str
    email: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Register Route --
@router.post("/register")
def register_user(req: RegisterRequest):
    user_id = add_user(
        req.username, 
        req.password,
        req.firstName,
        req.lastName,
        req.email
    )
    if user_id == -1:
        raise HTTPException(status_code=409, detail="Username already exists.")
    return {"user_id": user_id, "message": "User registered successfully"}

# Login Route --
@router.post("/login")
def login_user(req: LoginRequest):
    user_id = authenticate_user(req.username, req.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return {"user_id": user_id, "message": "Login successful."}

