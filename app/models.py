from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('now()'), nullable=False)

class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey(column="posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False, primary_key=True)