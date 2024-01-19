from flask import Blueprint
from flask_cors import cross_origin

from controller.work_controller import WorkController
from auth.auth import token_required
from common.field_common import TEAM, METHOD, ACCOUNT, WAGE, WORK

work = Blueprint("work", __name__)


@work.route(WORK.WORK, methods=[METHOD.POST])
# @cross_origin(origins="*")
@token_required
def insert_work():
    return WorkController().insert_work()


@work.route(WORK.WORK, methods=[METHOD.GET])
# @cross_origin(origins="*")
@token_required
def get_work():
    return WorkController().get_work()


@work.route(WORK.WORK_STAUT, methods=[METHOD.GET])
# @cross_origin(origins="*")
@token_required
def status_work():
    return WorkController().status_work()


@work.route(WORK.WORK_USER, methods=[METHOD.GET])
# @cross_origin(origins="*")
@token_required
def get_work_user():
    return WorkController().get_work_user()


@work.route(WORK.WORK_UPDATE, methods=[METHOD.PATCH])
# @cross_origin(origins="*")
@token_required
def update_done_work(id_work):
    return WorkController().update_done_work(id_work)