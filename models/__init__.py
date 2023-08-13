#!/usr/bin/python3
"""
This module instantiates:
An object of class FileStorage
OR
A database storage engine if env variable is "db"
"""

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
