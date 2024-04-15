from sqlalchemy import Column, Integer, String, BIGINT, VARCHAR, JSON
from sqlalchemy.orm import relationship

from database import Base


class Member(Base):
    __tablename__ = "member"

    member_id = Column(BIGINT, primary_key=True, index=True)
    member_guid = Column(VARCHAR(45), unique=True, index=True)
    member_insta_username = Column(VARCHAR(45), index=True)
    member_insta_id = Column(VARCHAR(45), index=True)
    member_insta_posting = Column(JSON)
    member_phone_id = Column(VARCHAR(45), index=True)
