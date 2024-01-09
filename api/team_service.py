from flask import Blueprint
from flask_cors import cross_origin

from controller.team_controller import TeamController
from auth.auth import token_required
from common.field_common import TEAM, METHOD, ACCOUNT

team = Blueprint("team", __name__)


@team.route(TEAM.TEAM, methods=[METHOD.POST])
#@cross_origin(origins="*")
@token_required
def create_team():
    return TeamController().create_team()


@team.route(TEAM.TEAM_UPDATE, methods=[METHOD.PATCH])
#@cross_origin(origins="*")
@token_required
def update_team(team_id):
    return TeamController().update_team(team_id)


@team.route(TEAM.TEAM_UPDATE, methods=[METHOD.POST])
#@cross_origin(origins="*")
@token_required
def delete_team():
    return TeamController().delete_team()


@team.route(TEAM.TEAM, methods=[METHOD.GET])
#@cross_origin(origins="*")
@token_required
def list_team():
    return TeamController().list_team()


@team.route(TEAM.TEAM_ACCOUNT, methods=[METHOD.POST])
#@cross_origin(origins="*")
@token_required
def get_info_account_by_id():
    return TeamController().get_info_account_by_id()


@team.route(TEAM.TEAM_UPDATE, methods=[METHOD.GET])
@token_required
def get_info_team(team_id):
    return TeamController().get_info_team(team_id)
