from pymongo import IndexModel, ASCENDING

from model.mongo.base_mongo_model import *


class AccountField:
    id = "id"
    fullname = "fullname"
    email = "email"
    username = "username"
    password = "password"
    role = "role"
    phone = "phone"

    all_field = [fullname, email, username, password, role, phone]

    class Role:
        admin = "admin"
        user = "user"
        client = "client"


class AccountModel(BaseMongo):

    def __init__(self, col=None, id=None, fullname=None, phone=None, username=None, password=None, role=None,
                 email=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["account"]
        self.id = id
        self.fullname = fullname
        self.phone = phone
        self.username = username
        self.password = password
        self.role = role
        self.email = email

    def create_account(self, this_moment):
        if not self.id or not self.fullname or not self.phone or not self.username or not self.password or not self.role or not self.email:
            return False

        data_insert = {
            AccountField.id: self.id,
            AccountField.fullname: self.fullname,
            AccountField.username: self.username,
            AccountField.password: self.password,
            AccountField.role: self.role,
            AccountField.phone: self.phone,
            AccountField.email: self.email,
            **this_moment
        }
        create_account = self.insert_one(data_insert)

        return create_account

    def sync_table(self):
        index_1 = IndexModel(
            [
                (AccountField.id, ASCENDING),
            ],
            background=True,
            unique=True,
        )
        index_2 = IndexModel(
            [
                (AccountField.id, ASCENDING),
                (AccountField.role, ASCENDING),
                (AccountField.username, ASCENDING),
            ],
            background=True,
            unique=False,
        )
        list_index = [index_1, index_2]
        self.add_index(list_index, is_drop_index=True)
