#!/usr/bin/python3
"""
store attributes in database
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.container import Container

classes = {'User': User, 'Container': Container}

classes


class DBStorage:
    """
    store object attribute in database
    """
    __engine = None
    __session = None

    def __init__(self):
        SD_MYSQL_USER = getenv('SD_MYSQL_USER')
        SD_MYSQL_PWD = getenv('SD_MYSQL_PWD')
        SD_MYSQL_HOST = getenv('SD_MYSQL_HOST')
        SD_MYSQL_DB = getenv('SD_MYSQL_DB')
        SD_ENV = getenv('SD_ENV')

        dburl = "mysql+mysqldb://{}:{}@{}/{}".format(SD_MYSQL_USER,
                                                     SD_MYSQL_PWD,
                                                     SD_MYSQL_HOST,
                                                     SD_MYSQL_DB)

        self.__engine = create_engine(dburl, pool_pre_ping=True)

        if SD_ENV == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """
        get all object based on their class name and if cls = None
        query all object types in Database
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj=None):
        """
        add object to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes to the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete object from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        create tables in database and create database session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def get(self, cls, id=None, username=None, image_id=None):
        """
        get user based on user id passed or  username
        """
        if cls:
            if id:
                obj = self.__session.query(cls).filter_by(id=id).first()
                return obj
            elif username:
                obj = self.__session.query(cls).filter_by(username=username).first()
                return obj
            elif image_id:
                obj = self.__session.query(cls).filter_by(image_id=image_id).first()
                return obj
        else:
            None

    def count(self, cls=None):
        """
        count entries in tables based on the class object passed
        """
        if cls:
            count = self.__session.query(cls).count()
            return count
        else:
            count = 0
            for class_name, class_obj in classes.items():
                count += self.__session.query(class_obj).count()
            return count

    def close(self):
        """
        close session
        """
        self.__session.close()
