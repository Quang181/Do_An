from model.mongo.base_mongo_model import *


class ProductModel(BaseMongo):
    name = "name"
    id_category = "id_category"
    price = "price"
    status = "status"
    describe = "describe"
    image = "image"

    all_field = [name, id_category, price, status, describe, image]

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["product"]
