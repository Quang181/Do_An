from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class CalenderCheckIn(BaseMongo):
    time = "time"
    update_on = "update_on"
    create_on = "create_on"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["calender_check_in"]
