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
def create_challenge(db: Session, title: str, description: str, flag: str) -> Challenge:
    db_challenge = Challenge(title=title, description=description, flag=flag)
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def get_challenge_by_id(db: Session, challenge_id: int) -> Optional[Challenge]:
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()

def get_challenge_by_title(db: Session, title: str) -> Optional[Challenge]:
    return db.query(Challenge).filter(Challenge.title == title).first()

def update_challenge(db: Session, challenge_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None, new_flag: Optional[str] = None) -> Optional[Challenge]:
    db_challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if db_challenge:
        if new_title:
            db_challenge.title = new_title
        if new_description:
            db_challenge.description = new_description
        if new_flag:
            db_challenge.flag = new_flag
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