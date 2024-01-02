from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class TeamModel(BaseMongo):
    id = "id"
    name = "name"
    update_on = "update_on"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["team"]
