#!/usr/bin/python3
"""
creat user class that inherit from BaseModel
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    user class that describes the user
    """
    first_name = None
    last_name = None
    username = None
    email = None
    password = None

    def __init__(self, *args, **kwargs):
        """
        inherit BaseModel methods and attributes
        """
        super().__init__(*args, **kwargs)
