#!/usr/bin/python3
"""
docker container class with it attribute
"""
from models.base_model import BaseModel
from datetime import datetime


class Container(BaseModel):
    """
    Container objects having all the necessart methods and
    attributes
    """
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
