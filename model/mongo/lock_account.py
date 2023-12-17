from pymongo import IndexModel, ASCENDING

from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class LockAccountModel(BaseMongo):
    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["lock_account"]

    account_id = "account_id"
    number_login = "number_login"
    time_login = "time_login"
    status = "status"

    def sync_table(self):
        index_1 = IndexModel(
            [
                (self.account_id, ASCENDING),
            ],
            background=True,
            unique=False,
        )

        list_index = [index_1]
        self.add_index(list_index, is_drop_index=True)
