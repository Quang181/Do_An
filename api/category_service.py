from flask import Blueprint
from controller.category_product_controller import CategoryProductController
from auth.auth import token_required
from common.field_common import CATEGORY, METHOD

category = Blueprint("category", __name__)


@category.route(CATEGORY.CATEGORY, methods=[METHOD.POST])
def add_category():
    return CategoryProductController().add_category()


@category.route(CATEGORY.UPDATE_CATEGORY, methods=[METHOD.PATCH])
def update_category(id_category):
    return CategoryProductController().update_category(id_category)


@category.route(CATEGORY.CATEGORY, methods=[METHOD.POST])
def delete_category():
    return CategoryProductController().delete_category()


@category.route(CATEGORY.CATEGORY, methods=[METHOD.GET])
def list_category():
    return CategoryProductController().list_category()


@category.route(CATEGORY.LIST_STATUS, methods=[METHOD.GET])
def list_status():
    return CategoryProductController().list_status()
