from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class CheckInProduct(BaseMongo):
    id = "id"
    id_product = "id_product"
    name = "name"
    cccd = "cccd"
    phone = "phone"
    email = "email"
    status = "status"
    time_check_in = "time_check_in"
    time_check_out = "time_check_out"
    id_account = "id_account"

    class Status:
        check_in = "check_in"
        check_out = "check_out"
        pre_order = "pre_order"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["check_in_product"]
