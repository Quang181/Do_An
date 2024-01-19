from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class WorkModel(BaseMongo):
    id = "id"
    account_id = "account_id"
    product_id = "product_id"
    describe = "describe"
    create_on = "create_on"
    update_on = "update_on"
    status = "status"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["work"]
