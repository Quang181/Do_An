from controller.base_controller import BaseController
from flask import request, jsonify
from model.team_model import Team

class TeamController(BaseController):

    def create_team(self):
        body = request.json
        name = body.get("name")


    def update_team(self):
        pass

    def delete_team(self, id_team):
        delete_team = Team.delete_team(id_team)
        if delete_team:
            return jsonify({"message": "Delete team success"}), 200
        else:
            return jsonify({"error": "Delete team not success"}), 500

    def get_list_team(self):
        body = request.json
        search = body.get("search")
        list_module = body.get("list_module")
        list_team = Team.get_list_team(search, list_module)
        list_team = list(list_team.dicts())
        return {"data": list_team}
