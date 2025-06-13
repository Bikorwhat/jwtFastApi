from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from internal.auth_service import signup, login
from internal.jwt_handler import create_token, verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from internal.db import get_db

router = APIRouter()
scheme= OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username:str
    email:str
    password:str
 
class LoginUser(BaseModel):
    email:str
    password:str


@router.post("/signup")
def signup_user(user: User, db: Session = Depends(get_db)):
    result = signup(user.username, user.email, user.password, db)
    if result:
        return {"message": "User created"}
    raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
def login_user(user: LoginUser, db: Session = Depends(get_db)):
    if login(user.email, user.password, db):
        access_token = create_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected route
@router.get("/protected")
def protected(token: str = Depends(scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": f"Hello {user['sub']}, you're authenticated!"}

