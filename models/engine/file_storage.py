 #!/usr/bin/python3
"""
serialize instance to a json file and deserializes json file to
instances
"""
import json
#from models.amenity import Amenity
from models.base_model import BaseModel
#from models.city import City
#from models.place import Place
#from models.review import Review
#from models.state import State
#from models.user import User

classes = {"BaseModel": BaseModel}


class FileStorage():
    """
    serialize instance to json file and deserialize json file
    object instance
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """return the dictionary of __objects"""
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
