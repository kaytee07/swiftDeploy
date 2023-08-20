#!/usr/bin/python3
"""
model for container object
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Datetime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Container(BaseModel, Base):
    """
    models important details about our docker container
    """
    __tablename__ = "container"

    status = Column(String(60), default="Stopped")
    container_id = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    start_time = Column(Datetime, default=datetime.utcnow)
    stop_time = Column(Datetime)

    user = relationship('User', back_populates='container')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
