from flask import Blueprint
from flask_cors import cross_origin

from controller.wage_account_controller import WageAccountController
from auth.auth import token_required
from common.field_common import TEAM, METHOD, ACCOUNT, WAGE

wage = Blueprint("wage", __name__)


@wage.route(WAGE.WAGE, methods=[METHOD.POST])
# @cross_origin(origins="*")
@token_required
def set_wage_account():
    return WageAccountController().set_wage_account()


@wage.route(WAGE.WAGE_UPDATE, methods=[METHOD.PATCH])
# @cross_origin(origins="*")
@token_required
def update_wage_account(account_id):
    return WageAccountController().update_wage_account(account_id)


@wage.route(WAGE.WAGE, methods=[METHOD.POST])
# @cross_origin(origins="*")
@token_required
def delete_wage():
    return WageAccountController().delete_wage()


@wage.route(WAGE.WAGE, methods=[METHOD.GET])
# @cross_origin(origins="*")
@token_required
def get_data_wage():
    return WageAccountController().get_data_wage()
