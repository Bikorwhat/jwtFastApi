from sqlalchemy.orm import Session
from .models import User
import bcrypt

def signup(username: str, email: str, password: str, db: Session):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return False
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    return True

def login(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return True
    return None
