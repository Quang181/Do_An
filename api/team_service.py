from flask import Blueprint
from controller.team_controller import TeamController
from auth.auth import token_required
from common.field_common import TEAM, METHOD, ACCOUNT

team = Blueprint("team", __name__)


@team.route(TEAM.TEAM, methods=[METHOD.POST])
def create_team():
    return TeamController().create_team()


@team.route(TEAM.TEAM_UPDATE, methods=[METHOD.PATCH])
def update_team(team_id):
    return TeamController().update_team(team_id)


@team.route(TEAM.TEAM_UPDATE, methods=[METHOD.POST])
def delete_team():
    return TeamController().delete_team()


@team.route(TEAM.TEAM, methods=[METHOD.GET])
def list_team():
    return TeamController().list_team()


@team.route(TEAM.TEAM_ACCOUNT, methods=[METHOD.POST])
def get_info_account_by_id():
    return TeamController().get_info_account_by_id()


@team.route(TEAM.TEAM_UPDATE, methods=[METHOD.GET])
def get_info_team(team_id):
    return TeamController().get_info_team(team_id)
