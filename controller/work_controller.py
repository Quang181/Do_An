import copy

from model.mongo.team_model import TeamModel
from model.mongo.team_assign import TeamAssignModel
from controller.base_controller import BaseController
from flask import request, jsonify
from pymongo import InsertOne, DESCENDING
from model.mongo.account_model import AccountModel, AccountField
from model.mongo.work_model import WorkModel


class WorkController(BaseController):

    def insert_work(self):
        body = request.json
        account_id = body.get(WorkModel.account_id)
        product_id = body.get(WorkModel.product_id)
        describe = body.get(WorkModel.describe)

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
        WorkModel().insert_one(data_insert)

        return {
            "code": 200,
            "data": data_return
        }

    def get_work(self):
        param = request.args
        paging = self.generate_paging_from_args(param)

        list_data = WorkModel().get_list_entity({}, paging, projection={"_id"})
        paginated = self.get_info_paging_for_response(list_data, paging)
        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    def get_work_user(self):
        param = request.args
        paging = self.generate_paging_from_args(param)
        id_account = self.get_info_in_token("id")

        list_data = WorkModel().get_list_entity({WorkModel.account_id: id_account}, paging, projection={"_id"})
        paginated = self.get_info_paging_for_response(list_data, paging)
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
