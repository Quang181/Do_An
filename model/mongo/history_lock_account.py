from pymongo import IndexModel, ASCENDING

from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class HistoryLockAccountModel(BaseMongo):
    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["history_lock_account"]