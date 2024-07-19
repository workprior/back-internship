from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.postgres_init import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    city = Column(String)
    phone = Column(String, unique=True)
    avatar = Column(String)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Record('{self.firstname}')"
