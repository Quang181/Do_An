from flask import Blueprint
from controller.product_controller import ProductController
from auth.auth import token_required
from common.field_common import PRODUCT, METHOD

product = Blueprint("product", __name__)


@product.route(PRODUCT.PRODUCT, methods=[METHOD.POST])
# @token_required
def create_product():
    return ProductController().create_product()


@product.route(PRODUCT.PRODUCT_UPDATE, methods=[METHOD.POST])
@token_required
def update_product(id_product):
    return ProductController().update_product(id_product)


@product.route(PRODUCT.PRODUCT, methods=[METHOD.POST])
@token_required
def delete_product():
    return ProductController().delete_product()


@product.route(PRODUCT.PRODUCT, methods=[METHOD.GET])
@token_required
def get_list_product():
    return ProductController().get_list_product()


@product.route(PRODUCT.PRE_ORDER, methods=[METHOD.POST])
@token_required
def pre_order():
    return ProductController().pre_order()


@product.route(PRODUCT.CHECK_IN, methods=[METHOD.PATCH])
@token_required
def check_in_room(id_order):
    return ProductController().check_in(id_order)


# @product.route(PRODUCT.CHECK_OUT, methods=[METHOD.POST])
# @token_required
# def get_list_product():
#     return ProductController().()

@product.route(PRODUCT.GET_PRICE_CHECK_OUT, methods=[METHOD.POST])
@token_required
def get_price_check_out():
    return ProductController().get_price_check_out()


@product.route(PRODUCT.STATUS_ORDER, methods=[METHOD.GET])
@token_required
def status_order():
    return ProductController().status_order()


@product.route(PRODUCT.ORDER, methods=[METHOD.GET])
@token_required
def list_order():
    return ProductController().list_order()


@product.route(PRODUCT.PRODUCT_VILA, methods=[METHOD.GET])
@token_required
def get_list_vila():
    return ProductController().get_list_vila()


@product.route(PRODUCT.PRODUCT_NOT_VILA, methods=[METHOD.GET])
@token_required
def get_list_product_not_vila():
    return ProductController().get_list_product_not_vila()


@product.route(PRODUCT.CHECK_OUT, methods=[METHOD.PATCH])
@token_required
def check_out(id_order):
    return ProductController().check_out(id_order)
