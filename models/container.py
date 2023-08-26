#!/usr/bin/python3
"""
docker container class with it attribute
"""
from models.base_model import BaseModel, Base
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from os import getenv

SD_TYPE_STORAGE = getenv('SD_TYPE_STORAGE')


class Container(BaseModel, Base):
    """
    Container objects having all the necessart methods and
    attributes
    """
    __tablename__ = 'containers'

    if SD_TYPE_STORAGE == 'db':
        name = Column(String(60), nullable=False)
        status = Column(String(60), nullable=False)
        container_id = Column(String(64), nullable=False)
        start_time = Column(DateTime)
        stop_time = Column(DateTime)
        user_id = Column(String(60), ForeignKey('users.id'))
    else:
        name = None
        status = None
        container_id = None
        start_time = None
        stop_time = None
        user_id = None

    def __init__(self, *args, **kwargs):
        """
        initializa attributes and inherit BaseModel attributes
        """
        super().__init__(*args, **kwargs)

    def start(self):
        """
        start docker container
        """
        self.start_time = datetime.utcnow()

    def stop(self):
        """
        stop docker container 
        """
        self.stop_time = datetime.utcnow()
