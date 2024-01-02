from flask import Blueprint
from controller.account_controller import AccountController
from auth.auth import token_required
from common.field_common import ACCOUNT, METHOD

account = Blueprint("account", __name__)


@account.route(ACCOUNT.LOGIN, methods=[METHOD.POST])
def login():
    return AccountController().login()


@account.route(ACCOUNT.ACCOUNT, methods=[METHOD.POST])
@token_required
def create_account():
    return AccountController().create_account()


@account.route(ACCOUNT.ACCOUNT_UPDATE, methods={METHOD.PATCH})
@token_required
def update_account(account_id):
    return AccountController().update_account(account_id)


@account.route(ACCOUNT.ACCOUNT, methods={METHOD.DELETE})
# @token_required
def delete_account():
    return AccountController().delete_account()


@account.route(ACCOUNT.FORGET_PASSWORD, methods={METHOD.POST})
def forget_password():
    return AccountController().forget_password()


@account.route(ACCOUNT.CHANGE_PASSWORD, methods={METHOD.POST})
def change_password():
    return AccountController().check_random_str()


@account.route(ACCOUNT.LIST_ROLE, methods={METHOD.GET})
def list_role():
    return AccountController().get_role()


@account.route(ACCOUNT.LIST_STATUS, methods={METHOD.GET})
def get_status():
    return AccountController().status_account()


@account.route(ACCOUNT.ACCOUNT, methods={METHOD.GET})
def get_list_account():
    return AccountController().get_list_account()


@account.route(ACCOUNT.DETAIL_ACCOUNT, methods={METHOD.GET})
def detail_account(account_id):
    return AccountController().detail_account(account_id)


@account.route(ACCOUNT.ACCOUNT_CLIENT, methods={METHOD.POST})
def create_account_client():
    return AccountController().create_account_client()


@account.route(ACCOUNT.ACCOUNT_CLIENT, methods={METHOD.POST})
def get_info_account_by_ids():
    return AccountController().get_info_account_by_ids()


@account.route(ACCOUNT.ACCOUNT_CHECK_IN, methods={METHOD.POST})
def check_in_account():
    return AccountController().check_in_account()


@account.route(ACCOUNT.GET_WAGE, methods={METHOD.GET})
def get_wage_account():
    return AccountController().get_wage_account()


@account.route(ACCOUNT.ACCOUNT_NOT_TEAM, methods={METHOD.GET})
def account_not_in_team():
    return AccountController().account_not_in_team()
