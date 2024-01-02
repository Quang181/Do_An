from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class CheckIn(BaseMongo):
    account_id = "account_id"
    time = "time"
    update_on = "update_on"
    create_on = "create_on"
    time_work = "time_work"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["check_in"]
