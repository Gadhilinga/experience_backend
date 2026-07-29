from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)

    @property
    def mobile(self):
        return self.phone

    @mobile.setter
    def mobile(self, value):
        self.phone = value