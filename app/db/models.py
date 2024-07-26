from sqlalchemy import Boolean, Column, Integer, String

from app.db.postgres_init import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    lastname = Column(String, nullable=False)
    city = Column(String)
    phone = Column(String, unique=True)

    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"Record('{self.firstname}')"
