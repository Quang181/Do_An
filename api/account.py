from flask import Blueprint
from controller.account_controller import AccountController
from auth.auth import token_required
from common.field_common import ACCOUNT, METHOD
from flask_cors import cross_origin
account = Blueprint("account", __name__)


@account.route(ACCOUNT.LOGIN, methods=[METHOD.POST])
#@cross_origin(origins="*")
def login():
    return AccountController().login()


@account.route(ACCOUNT.ACCOUNT, methods=[METHOD.POST])
#@cross_origin(origins="*")
@token_required
def create_account():
    return AccountController().create_account()


@account.route(ACCOUNT.ACCOUNT_UPDATE, methods={METHOD.PATCH})
#@cross_origin(origins="*")
@token_required
def update_account(account_id):
    return AccountController().update_account(account_id)


@account.route(ACCOUNT.ACCOUNT, methods={METHOD.DELETE})
#@cross_origin(origins="*")
@token_required
def delete_account():
    return AccountController().delete_account()


@account.route(ACCOUNT.FORGET_PASSWORD, methods={METHOD.POST})
#@cross_origin(origins="*")
def forget_password():
    return AccountController().forget_password()


@account.route(ACCOUNT.CHANGE_PASSWORD, methods={METHOD.POST})
#@cross_origin(origins="*")
def change_password():
    return AccountController().check_random_str()


@account.route(ACCOUNT.LIST_ROLE, methods={METHOD.GET})
@token_required
def list_role():
    return AccountController().get_role()


@account.route(ACCOUNT.LIST_STATUS, methods={METHOD.GET})
@token_required
def get_status():
    return AccountController().status_account()


@account.route(ACCOUNT.ACCOUNT, methods={METHOD.GET})
@token_required
def get_list_account():
    return AccountController().get_list_account()


@account.route(ACCOUNT.DETAIL_ACCOUNT, methods={METHOD.GET})
@token_required
def detail_account(account_id):
    return AccountController().detail_account(account_id)


@account.route(ACCOUNT.ACCOUNT_CLIENT, methods={METHOD.POST})
@token_required
def create_account_client():
    return AccountController().create_account_client()


@account.route(ACCOUNT.ACCOUNT_CLIENT, methods={METHOD.POST})
@token_required
def get_info_account_by_ids():
    return AccountController().get_info_account_by_ids()


@account.route(ACCOUNT.ACCOUNT_CHECK_IN, methods={METHOD.POST})
@token_required
def check_in_account():
    return AccountController().check_in_account()


@account.route(ACCOUNT.GET_WAGE, methods={METHOD.GET})
@token_required
def get_wage_account(account_id):
    return AccountController().get_wage_account(account_id)


@account.route(ACCOUNT.ACCOUNT_NOT_TEAM, methods={METHOD.GET})
@token_required
def account_not_in_team():
    return AccountController().account_not_in_team()


@account.route(ACCOUNT.CHECK_DAY_CHECK_In, methods={METHOD.GET})
@token_required
def check_day_check_in():
    return AccountController().check_day_check_in()


@account.route(ACCOUNT.ACCOUNT_CHECK_IN_DAY, methods={METHOD.GET})
@token_required
def list_account_check_in_by_day():
    return AccountController().list_account_check_in_by_day()


@account.route(ACCOUNT.ACCOUNT_NOT_CLIENT, methods={METHOD.GET})
@token_required
def list_account_not_client():
    return AccountController().list_account_not_client()
