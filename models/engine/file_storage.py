 #!/usr/bin/python3
"""
serialize instance to a json file and deserializes json file to
instances
"""
import json
#from models.docker import images
from models.base_model import BaseModel
from models.container import Container
from models.user import User

classes = {"BaseModel": BaseModel, "User": User, "Container": Container}


class FileStorage():
    """
    serialize instance to json file and deserialize json file
    object instance
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """return the dictionary of __objects"""
        new_object = {}
        if cls:
            for key, value in self.__objects.items():
                print(value.to_dict())
                cls_name = str(cls).split(".")[2].split("'")[0]
                if value.to_dict()['__class__'] == cls_name:
                    new_object[key] = value
            return new_object
        else:
            return self.__objects

    def new(self, obj):
        """ set key, value in __objects"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        serialize __objects to the JSON file
        (path:__file_path)
        """
        data = {}
        for key, value in self.__objects.items():
            data[key] = value.to_dict()
        with open(self.__file_path, 'w') as files:
            json.dump(data, files)

    def reload(self):
        """
        deserialize json file to object
        """
        with open(self.__file_path, 'r') as files:
            json_data = json.load(files)
            for key in json_data:
                self.__objects[key] = classes[key.split('.')[0]](**json_data[key])

    def delete(self, obj=None):
        if obj:
            key = f"{obj.to_dict()['__class__']}.{obj.to_dict()['id']}"
            del self.__objects[key]
