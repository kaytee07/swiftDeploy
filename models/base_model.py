#!/usr/bin/python3
"""
this class object defines common attributes and models like the id
, time of creation and time of update which will be a part of all
models we create
"""
import uuid
import sys
from datetime import datetime
import models
from sqlalchemy import Column, Integer, String, create_engine, Datetime
from sqlalchemy.ext.declarative import declarative_base


time = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()


class BaseModel():
    """
    this class object defines common attributes and models
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(Datetime, default=datetime.utcnow)
    updated_at = Column(Datetime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """initialize class attributes"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        date_obj = datetime.strptime(value, time)
                        setattr(self, key, date_obj)
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()

    def __str__(self):
        """Represent class in a string form"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """update the updated_at atribute"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """delete current instance from storage"""
        models.storage.delete(self)

    def to_dict(self):
        """
        return dictionary containing all key values of __dict__
        of the instance with new key class
        """
        new_dict = {}
        new_dict['__class__'] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key == 'updated_at' or key == 'created_at':
                new_dict[key] = value.strftime(time)
            else:
                new_dict[key] = value
        return new_dict
