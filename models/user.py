#!/usr/bin/python3
"""
creat user class that inherit from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

SD_TYPE_STORAGE = getenv('SD_TYPE_STORAGE')

class User(BaseModel, Base):
    """
    user class that describes the user
    """
    __tablename__ = 'users'

    if SD_TYPE_STORAGE == 'db':
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        username = Column(String(60), nullable=False)
        email = Column(String(60), nullable=False)
        password = Column(String(60), nullable=False)
        salt = Column(String(128), nullable=False)
        container = relationship('Container', backref='user')
    else:
        first_name = None
        last_name = None
        username = None
        email = None
        salt = None
        password = None

    def __init__(self, *args, **kwargs):
        """
        inherit BaseModel methods and attributes
        """
        super().__init__(*args, **kwargs)
