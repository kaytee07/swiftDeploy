 #!/usr/bin/python3
"""
store object value in database
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBStorage():
    """
    CRUD using database tables
    """
    __engine = None
    _session = None

    def __init__(self):
        """
        create session engine and link it to the database
        """
        SD_MYSQL_USER = getenv('SD_MYSQL_USER')
        SD_MYSQL_PWD = getenv('SD_MYSQL_PWD')
        SD_MYSQL_HOST = getenv('SD_MYSQL_HOST')
        SD_MYSQL_DB = getenv('SD_MYSQL_DB')
        SD_ENV = getenv('SD_ENV')
        self.__engine = create_engine("mysql+mysqldb://{}.{}@{}/{}"
                                      .format(SD_MYSQL_USER,
                                              SD_MYSQL_PWD,
                                              SD_MYSQL_HOST,
                                              SD_MYSQL_DB))
