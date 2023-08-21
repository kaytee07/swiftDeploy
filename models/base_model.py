#!/usr/bin/python3
"""
defines the common attribute for all other classes 
"""
import uuid
from datetime import datetime

time_fmt = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """
    attributes common to all other classes
    """
    def __init__(self):
        """
        initialize class attributes
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        new_dict = {}
        new_dict['__class__'] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key == 'updated_at' or key == 'created_at':
                new_dict[key] = value.strftime(time_fmt)
            else:
                new_dict[key] = value
        return new_dict
