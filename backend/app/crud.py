from sqlalchemy.orm import Session
from app.models import User, Challenge
from typing import Optional

# CRUD operations for User
def create_user(db: Session, username: str, password_hash: str, is_admin: bool) -> User:
    db_user = User(username=username, password_hash=password_hash, is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def update_user(db: Session, user_id: int, new_username: Optional[str] = None, new_password_hash: Optional[str] = None) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if new_username:
            db_user.username = new_username
        if new_password_hash:
            db_user.password_hash = new_password_hash
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# CRUD operations for Challenge
def create_challenge(db: Session, id: int, name: str, story: str, description: str,
                     difficulty: str, flag: str) -> Challenge:
    db_challenge = Challenge(id=id, name=name, story=story,description=description,
                             difficulty=difficulty, flag=flag)
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def get_challenge_by_id(db: Session, challenge_id: int) -> Optional[Challenge]:
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()

def get_challenge_by_title(db: Session, name: str) -> Optional[Challenge]:
    return db.query(Challenge).filter(Challenge.name == name).first()

def update_challenge(db: Session, challenge_id: int, **kwargs) -> Optional[Challenge]:
    db_challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if db_challenge:
        for key, value in kwargs.items():
            setattr(db_challenge, key, value)
        db.commit()
        db.refresh(db_challenge)
        return db_challenge
    return None

def delete_challenge(db: Session, challenge_id: int) -> bool:
    db_challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if db_challenge:
        db.delete(db_challenge)
        db.commit()
        return True
    return False