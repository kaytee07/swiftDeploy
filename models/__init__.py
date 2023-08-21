#!/usr/bin/python3
"""
create instance of file storage and deserialze json file
"""
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
