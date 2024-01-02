from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class WageAccountModel(BaseMongo):
    account_id = "account_id"
    wage = "wage"
    update_on = "update_on"
    insert_on = "insert_on"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["wage_account"]
