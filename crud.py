from sqlalchemy.orm import Session
from models import Member

def get_member(db: Session, member_insta_username: int):
    return db.query(Member).filter(Member.member_insta_username == member_insta_username).first()

def get_memberById(db: Session, member_id: int):
    return db.query(Member).filter(Member.member_id == member_id).first()