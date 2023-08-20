#!/usr/bin/python3
"""
User class that inherit from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(Base, BaseModel):
    """
    User models important details about our user object
    """
    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)

    container = relationship('Container', back_populates='user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
