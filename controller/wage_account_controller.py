from controller.base_controller import BaseController
from model.mongo.wage_account_model import WageAccountModel
from model.mongo.account_model import AccountModel, AccountField
from flask import request, jsonify


class WageAccountController(BaseController):

    def set_wage_account(self):
        body = request.json
        account_id = body.get("account_id")
        wage = body.get("wage")

        if WageAccountModel().filter_one({WageAccountModel.account_id: account_id}):
            return jsonify(self.get_error("Nhân viên đã có mức lương từ trước đó")), 413
        insert_data = WageAccountModel().insert_one({
            WageAccountModel.account_id: account_id,
            WageAccountModel.wage: wage,
            **self.this_moment_create()})

        if insert_data:
            return {
                "code": 200,
                "data": body
            }

        return jsonify(self.get_error("Insert not success")), 413

    def update_wage_account(self, account_id):
        wage = request.json.get("wage", 0)
        if not WageAccountModel().filter_one({WageAccountModel.account_id: account_id}):
            return jsonify(self.get_error("Không có dữ liệu để update ")), 413
        update_data = WageAccountModel().update_one({WageAccountModel.account_id: account_id},
                                                    {WageAccountModel.wage: wage})
        if update_data:
            return {
                "code": 200,
                "data": request.json
            }

        return jsonify(self.get_error("Update fail")), 413

    def delete_wage(self):
        body = request.json
        account_ids = body.get("account_ids")
        delete_data = WageAccountModel().delete_many_data({WageAccountModel.account_id: {"$in": account_ids}})
        if delete_data:
            return {
                "code": 200
            }
        return jsonify(self.get_error("delete data fail")), 413

    def get_data_wage(self):
        param = request.args
        paging = self.generate_paging_from_args(param)
        list_data_wage = WageAccountModel().get_list_entity({}, paging)

        paginated = self.get_info_paging_for_response(list_data_wage, paging)
        account_ids = [i.get(WageAccountModel.account_id) for i in list_data_wage.get("list_data")]

        data_convert = {}
        if account_ids:
            list_account = AccountModel().find({AccountField.id: {"$in": account_ids}})
            for i in list_account:
                account_id = i.get(AccountField.id)
                fullname = i.get(AccountField.fullname)
                phonenumber = i.get(AccountField.phone)
                email = i.get(AccountField.email)

                data_convert.update({account_id: {
                    AccountField.id: account_id,
                    AccountField.fullname: fullname,
                    AccountField.phone: phonenumber,
                    AccountField.email: email
                }})
        for i in list_data_wage.get("list_data"):
            account_id = i.get(WageAccountModel.account_id)
            if account_id in data_convert:
                i.update({"account": data_convert.get(account_id)})

        return {
            "code": 200,
            "data": list_data_wage.get("list_data"),
            "paging": paginated
        }

