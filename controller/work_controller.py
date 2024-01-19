import copy

from model.mongo.team_model import TeamModel
from model.mongo.team_assign import TeamAssignModel
from controller.base_controller import BaseController
from flask import request, jsonify
from pymongo import InsertOne, DESCENDING
from model.mongo.account_model import AccountModel, AccountField
from model.mongo.work_model import WorkModel
from model.mongo.product_model import ProductModel

class WorkController(BaseController):

    def insert_work(self):
        body = request.json
        account_id = body.get(WorkModel.account_id)
        product_id = body.get(WorkModel.product_id)
        describe = body.get(WorkModel.describe)
        info_account = AccountModel().filter_one({AccountField.id: account_id} , projection={"_id": 0})
        if not info_account:
            return jsonify(self.get_error("Account not exits")), 413
        info_product = ProductModel().filter_one({ProductModel.id: product_id}, projection={"_id": 0})
        if not info_product:
            return jsonify(self.get_error("Product not exits")), 413

        id = self.generate_uuid()
        data_insert = {
            WorkModel.product_id: product_id,
            WorkModel.account_id: account_id,
            WorkModel.id: id,
            WorkModel.describe: describe,
            "status": "new",
            **self.this_moment_create()
        }
        data_return = copy.deepcopy(data_insert)
        data_return.update({"account": info_account,
                            "product": info_product})
        WorkModel().insert_one(data_insert)

        return {
            "code": 200,
            "data": data_return
        }

    def get_work(self):
        param = request.args
        paging = self.generate_paging_from_args(param)

        list_data = WorkModel().get_list_entity({}, paging, projection={"_id": 0})
        ids_account = [i.get(WorkModel.account_id) for i in list_data.get("list_data")]
        ids_product = [i.get(WorkModel.product_id) for i in list_data.get("list_data")]

        list_account = AccountModel().find({AccountField.id: {"$in": ids_account}}, projection={"_id": 0})
        # if not list_account:
        #     return jsonify(self.get_error("Account not exits")), 413
        list_product = ProductModel().find({ProductModel.id: {"$in": ids_product}}, projection={"_id": 0})
        # if not list_product:
        #     return jsonify(self.get_error("Product not exits")), 413

        convert_account = {}
        convert_product = {}
        for i in list_account:
            account_id = i.get(AccountField.id)
            convert_account.update({account_id: i})

        for i in list_product:
            product_id = i.get(ProductModel.id)
            convert_product.update({product_id: i})

        paginated = self.get_info_paging_for_response(list_data, paging)
        for i in list_data.get("list_data"):
            account_id = i.get(WorkModel.account_id)
            product_id = i.get(WorkModel.product_id)

            i.update({"account": convert_account.get(account_id, {}),
                      "product": convert_product.get(product_id, {})})
        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    def get_work_user(self):
        param = request.args
        paging = self.generate_paging_from_args(param)
        id_account = self.get_info_in_token("id")

        list_data = WorkModel().get_list_entity({WorkModel.account_id: id_account}, paging, projection={"_id": 0})
        paginated = self.get_info_paging_for_response(list_data, paging)

        ids_account = [i.get(WorkModel.account_id) for i in list_data.get("list_data")]
        ids_product = [i.get(WorkModel.product_id) for i in list_data.get("list_data")]
        list_account = AccountModel().find({AccountField.id: {"$in": ids_account}}, projection={"_id": 0})
        # if not list_account:
        #     return jsonify(self.get_error("Account not exits")), 413
        list_product = ProductModel().find({ProductModel.id: {"$in": ids_product}}, projection={"_id": 0})
        # if not list_product:
        #     return jsonify(self.get_error("Product not exits")), 413

        convert_account = {}
        convert_product = {}
        for i in list_account:
            account_id = i.get(AccountField.id)
            convert_account.update({account_id: i})

        for i in list_product:
            product_id = i.get(ProductModel.id)
            convert_product.update({product_id: i})

        for i in list_data.get("list_data"):
            account_id = i.get(WorkModel.account_id)
            product_id = i.get(WorkModel.product_id)

            i.update({"account": convert_account.get(account_id, {}),
                      "product": convert_product.get(product_id, {})})
        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    def update_done_work(self, id_work):
        id_account = self.get_info_in_token("id")
        check_exits = WorkModel().filter_one({WorkModel.id: id_work}, projection={"_id"})
        data_return = copy.deepcopy(check_exits)
        if not check_exits:
            return jsonify(self.get_error("Work not exist")), 413

        if check_exits.get(WorkModel.account_id) != id_account:
            return jsonify(self.get_error("Khong co quyen")), 413

        WorkModel().update_one({WorkModel.id: id_work}, {WorkModel.status: "done",
                                                         **self.this_moment_update()})

        data_return.update({WorkModel.status: "done"})
        return {
            "code": 200,
            "data": data_return
        }

    def status_work(self):

        return {
            "code": 200,
            "data": [
                        {
                            "key": "done",
                            "name": "Hoàn thành"
                        },
                        {
                            "key": "new",
                            "name": "Mới"
                        }
    ]
        }
