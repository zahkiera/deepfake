from fastapi import APIRouter, HTTPException, Query, Depends


from pydantic import BaseModel, constr
from db import add_user, authenticate_user, get_connection
import sqlite3



# db helper functions
from db import update_username, update_password, get_email
from db import delete_user_by_username, update_email as db_update_email

router = APIRouter()

def get_connection():
    return sqlite3.connect("DeepfakeGame.db")

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

class UpdateUsernameRequest(BaseModel):
    username: str
    password: str
    new_username: str

class EmailRequest(BaseModel):
    username: str
    password: str

class UpdateEmailRequest(BaseModel):
    username: str
    password: str
    email: str
    new_email: str

class UpdatePasswordInSettingsRequest(BaseModel):
    username: str
    current_password: str
    new_password: constr(min_length=10)


class DeactivateUserRequest(BaseModel):
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
    # check username exists
    if user_id == -1:
        raise HTTPException(status_code=409, detail="Username already exists.")
    # check email alr exists
    elif user_id == -2:
        raise HTTPException(status_code=409, detail="Email already exists.")

    return {"user_id": user_id, "message": "User registered successfully"}

# Login Route --
@router.post("/login")
def login_user(req: LoginRequest):
    user_id = authenticate_user(req.username, req.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return {"user_id": user_id, "message": "Login successful."}

### Setting Routes


# Usernames
@router.put("/update-username") 
def update_user(req: UpdateUsernameRequest):
    user_id = authenticate_user(req.username, req.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
        
    if req.new_username:  
        result = update_username(user_id, req.new_username)
        if result == -1:
            raise HTTPException(status_code=409, detail="Username already exists.")
            
        return {"message": "Username updated successfully"}

@router.put("/update-email") 
def update_email(req: UpdateEmailRequest):
    user_id = authenticate_user(req.username, req.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
        
    if req.new_email:  
        result = db_update_email(user_id, req.new_email)
        if result == -1:
            raise HTTPException(status_code=409, detail="Email already exists.")
            
        return {"message": "Email updated successfully"}

@router.get('/email')
def get_user_email(username:str, password:str):
    user_id = authenticate_user(username, password)
    email = get_email(user_id)  
    return {'email': email}

    
# Update pass (for logged in users)
@router.put("/update-password")
def update_password_in_settings(req: UpdatePasswordInSettingsRequest):
    # Step 1: Verify current password
    user_id = authenticate_user(req.username, req.current_password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    # Step 2: Update password
    update_password(user_id, req.new_password)
    return {"message": "Password updated successfully."}

# Deactivate
@router.post("/deactivate")
def deactivate_user(req: DeactivateUserRequest):
    try:
        # Verify user before deactivation
        user_id = authenticate_user(req.username, req.password)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials.")
            
        result = delete_user_by_username(req.username)
        if result:
            return {"message": "Account deactivated successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to deactivate account")
    except Exception as e:
        # Log the error
        print(f"Error in deactivate_user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        

