from model.mongo.base_mongo_model import *


class CategoryProductModel(BaseMongo):
    name = "name"
    _ID = "_id"
    id = "id"
    status = "status"
    describe = "describe"
    update_on ="update_one"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["category_product"]
