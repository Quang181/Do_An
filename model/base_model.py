import os
from peewee import *

name_db = os.environ.get("NAME_DB")
password_db = os.environ.get("PASSWORD_DB")
host = os.environ.get("HOST_DB")
port_db = os.environ.get("PORT_DB")
username = os.environ.get("USERNAME_DB")
db = MySQLDatabase(name_db, host=host, port=int(port_db), user=username, password=password_db)


class BaseModel(Model):
    class Meta:
        database = db
