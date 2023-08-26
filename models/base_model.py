#!/usr/bin/python3
"""
defines the common attribute for all other classes 
"""
import uuid
from datetime import datetime
import models
import binascii
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
time_fmt = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """
    attributes common to all other classes
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        initialize class attributes
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    pass
                elif key == 'created_at' or key == 'updated_at' or key == 'start_time' or key == 'stop_time':
                    date_obj = datetime.strptime(value, time_fmt)
                    setattr(self, key, date_obj)
                else:
                    setattr(self, key, value)
                if kwargs.get("id", None) is None:
                    self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def __str__(self):
        """this is going to be the string representation of the class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """update public instance attribute"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, db=None):
        """dictionary representation of all attribute in class"""
        new_dict = {}
        new_dict['__class__'] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key == 'updated_at' or key == 'created_at' or key == 'start_time' or key == 'stop_time':
                new_dict[key] = value.strftime(time_fmt)
            elif key == '_sa_instance_state':
                pass
            elif db:
                if key == 'password':
                    pass
            elif key == 'salt':
                new_dict[key] = binascii.hexlify(value).decode('utf-8')
            else:
                new_dict[key] = value
        return new_dict

    def delete(self):
        """delete current class instance from storage"""
        models.storage.delete(self)
