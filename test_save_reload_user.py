#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User


all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User --")
my_user = User()
my_user.first_name = "Benjamin"
my_user.last_name = "Maine"
my_user.email = "benmaine@imail.com"
my_user.password = "bentmaine"
my_user.username = "uncmaine"
my_user.dockerID = "bentaminter"
my_user.save()
print(my_user)

print("-- Create a new User 3 --")
my_user3 = User()
my_user3.first_name = "Natasha"
my_user3.last_name = "Ntreh"
my_user3.email = "ntreh07@imail.com"
my_user3.password = "natash11"
my_user3.username = "naatiorkor"
my_user3.dockerID = "natasha12"
my_user.save()
print(my_user)

print("-- Create a new User 4 --")
my_user1 = User()
my_user1.first_name = "lisa"
my_user1.last_name = "Turkson"
my_user1.email = "lisa07@imail.com"
my_user1.password = "lisaturk"
my_user1.username = "Monalisa"
my_user1.dockerID = "Lisannea2"
my_user.save()
print(my_user)

print("-- Create a new User 2 --")
my_user2 = User()
my_user2.first_name = "Canadian"
my_user2.last_name = "goose"
my_user2.email = "kyle1@omail.com"
my_user2.password = "cango111"
my_user2.username = "cangoose"
my_user2.dockerID = "dockeenaa"
my_user2.save()
print(my_user2)
