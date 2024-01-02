from model.mongo.base_mongo_model import *


class ProductModel(BaseMongo):
    id = "id"
    name = "name"
    id_category = "id_category"
    price = "price"
    status = "status"
    describe = "describe"
    image = "image"
    account_id = "account_id"

    all_field = [name, id_category, price, status, describe, image]

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["product"]
#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