from model.mongo.team_model import TeamModel
from model.mongo.team_assign import TeamAssignModel
from controller.base_controller import BaseController
from flask import request, jsonify
from pymongo import InsertOne, DESCENDING
from model.mongo.account_model import AccountModel, AccountField


class TeamController(BaseController):

    def create_team(self):
        body = request.json

        name = body.get(TeamModel.name)
        accounts = body.get("accounts")
        if not name:
            return jsonify(self.get_error("Tên team không được để trống ")), 413

        check_exits = TeamModel().filter_one({TeamModel.name: name})
        if check_exits:
            return jsonify(self.get_error("Tên team đã tồn tại ")), 413
        if accounts:
            id_account = [i.get(TeamAssignModel.id_account) for i in accounts]

            check_exits = TeamAssignModel().find({TeamAssignModel.id_account: {"$in": id_account}})

            check_account = AccountModel().find({AccountField.id: {"$in": id_account}})
            if len(check_account) != len(id_account):
                return jsonify(self.get_error("Account không tồn tại ")), 413

            if check_exits:
                return jsonify(self.get_error("Một nhân viên nào đó đã tồn tại trong team khác ")), 413

        id_team = self.generate_uuid()

        TeamModel().insert_one({TeamModel.id: id_team,
                                TeamModel.name: name,
                                **self.this_moment_create()})
        team_assign_bulk = []
        for account in accounts:
            id_account = account.get("id_account")
            position = account.get(TeamAssignModel.position)

            team_assign_bulk.append(InsertOne({TeamAssignModel.id_account: id_account,
                                               TeamAssignModel.position: position,
                                               TeamAssignModel.id_team: id_team,
                                               **self.this_moment_create()}))
        if team_assign_bulk:
            TeamAssignModel().bulk_write(team_assign_bulk)
        body.update({TeamModel.id: id_team})

        return {
            "code": 200,
            "data": body
        }

    def update_team(self, id_team):
        body = request.json

        name = body.get(TeamModel.name)
        accounts = body.get("accounts")

        if not TeamModel().find({TeamModel.id: id_team}):
            return jsonify(self.get_error("Team không tồn tại ")), 413

        if accounts:
            id_account = [i.get(TeamAssignModel.id_account) for i in accounts]

            check_exits = TeamAssignModel().find({TeamAssignModel.id_account: {"$in": id_account},
                                                  TeamAssignModel.id_team: {"$ne": id_team}})
            if check_exits:
                return jsonify(self.get_error("Một nhân viên nào đó đã tồn tại trong team khác ")), 413

        if name:
            TeamModel().update_one({TeamModel.id: id_team}, {TeamModel.name: name})

        TeamAssignModel().delete_many_data({TeamAssignModel.id_team: id_team})

        team_assign_bulk = []
        for account in accounts:
            id_account = account.get("id_account")
            position = account.get(TeamAssignModel.position)

            team_assign_bulk.append(InsertOne({TeamAssignModel.id_account: id_account,
                                               TeamAssignModel.position: position,
                                               TeamAssignModel.id_team: id_team,
                                               **self.this_moment_create()}))
        if team_assign_bulk:
            TeamAssignModel().bulk_write(team_assign_bulk)

        return {
            "code": 200,
            "data": body
        }

    def delete_team(self):
        body = request.json
        ids_team = body.get("ids_team")
        if not ids_team:
            return jsonify(self.get_error("Id team không được để trống ")), 413
        check_exits = TeamModel().find({TeamModel.id: {"$in": ids_team}})
        if len(ids_team) != len(check_exits):
            return jsonify(self.get_error("Team không tồn tại ")), 413

        TeamModel().delete_many_data({TeamModel.id: ids_team})
        TeamAssignModel().delete_many_data({TeamAssignModel.id_team: ids_team})

        return {
            "code": 200
        }

    def list_team(self):
        params = request.args
        search = params.get("search")
        paging = self.generate_paging_from_args(params)

        query = {}
        if search:
            query.update({TeamModel.name: search})

        list_data = TeamModel().get_list_entity(query, paging, {"_id": 0},
                                                sort_options=[(TeamModel.update_on, DESCENDING)])
        paginated = self.get_info_paging_for_response(list_data, paging)

        ids_team = [i.get(TeamModel.id) for i in list_data.get("list_data")]

        convert_account_by_team = {}
        if ids_team:
            list_account = TeamAssignModel().find({TeamAssignModel.id_team: {"$in": ids_team}})

            for account_assign in list_account:
                id_team = account_assign.get(TeamAssignModel.id_team)
                id_account = account_assign.get(TeamAssignModel.id_account)

                if id_team in convert_account_by_team:
                    convert_account_by_team.get(id_team).append(id_account)
                else:
                    convert_account_by_team.update({id_team: [id_account]})
        for team in list_data.get("list_data"):
            id_team = team.get(TeamModel.id)

            team.update({"accounts": convert_account_by_team.get(id_team, [])})

        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    def get_info_account_by_id(self):
        body = request.json

        accounts = body.get("accounts")
        if not accounts:
            return {
                "code": 200,
                "data": []
            }
        projection = {
            "_id": 0,
            AccountField.phone: 1,
            AccountField.id: 1,
            AccountField.fullname: 1,
            AccountField.email: 1,

        }
        list_account = AccountModel().find({AccountField.id: {"$in": accounts}}, projection=projection)

        ids_account = [i.get("id") for i in list_account]
        team_assign = TeamAssignModel().find({TeamAssignModel.id_account: {"$in": ids_account}})

        data_convert = {}
        for i in team_assign:
            id_account = i.get(TeamAssignModel.id_account)
            position = i.get(TeamAssignModel.position)

            data_convert.update({id_account: position})

        for i in list_account:
            id_account = i.get(AccountField.id)

            i.update({TeamAssignModel.position: data_convert.get(id_account)})

        return {
            "code": 200,
            "data": list_account
        }

    def get_info_team(self, id_team):
        check_exist = TeamModel().filter_one({TeamModel.id: id_team}, {"_id": 0})
        if not check_exist:
            return jsonify(self.get_error("Team không tồn tại ")), 413

        team_assign = TeamAssignModel().find({TeamAssignModel.id_team: id_team})

        list_id_account = []
        list_convert = {}
        for i in team_assign:
            id_account = i.get(TeamAssignModel.id_account)
            position = i.get(TeamAssignModel.position)

            list_id_account.append(id_account)
            list_convert.update({id_account: {TeamAssignModel.position: position}})

        if list_id_account:
            projection = {
                "_id": 0,
                AccountField.phone: 1,
                AccountField.id: 1,
                AccountField.fullname: 1,
                AccountField.email: 1,

            }

            list_account = AccountModel().find({AccountField.id: {"$in": list_id_account}}, projection=projection)
            for account in list_account:
                id_account = account.get(AccountField.id)
                list_convert.get(id_account).update({**account})

        if list_convert:
            accounts = []
            for k, v in list_convert.items():
                accounts.append(v)
            check_exist.update({"accounts": accounts})
        return {
            "code": 200,
            "data": check_exist
        }