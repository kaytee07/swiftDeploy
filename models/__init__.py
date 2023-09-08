#!/usr/bin/python3
"""
create instance of file storage and deserialze json file
"""
from os import getenv

SD_TYPE_STORAGE = getenv('SD_TYPE_STORAGE')
if SD_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
