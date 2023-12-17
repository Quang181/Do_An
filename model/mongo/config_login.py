from model.mongo.base_mongo_model import *


class ConfigLogin(BaseMongo):

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["lock_account"]
