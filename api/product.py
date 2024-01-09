from flask import Blueprint
from flask_cors import cross_origin

from controller.product_controller import ProductController
from auth.auth import token_required
from common.field_common import PRODUCT, METHOD

product = Blueprint("product", __name__)


@product.route(PRODUCT.PRODUCT_UPDATE, methods=[METHOD.POST])
#@cross_origin(origins="*")
@token_required
def create_product():
    return ProductController().create_product()


@product.route(PRODUCT.PRODUCT_UPDATE, methods=[METHOD.PATCH])
#@cross_origin(origins="*")
@token_required
def update_product(id_product):
    return ProductController().update_product(id_product)


@product.route(PRODUCT.PRODUCT, methods=[METHOD.POST])
#@cross_origin(origins="*")
@token_required
def delete_product():
    return ProductController().delete_product()


@product.route(PRODUCT.PRODUCT, methods=[METHOD.GET])
#@cross_origin(origins="*")
@token_required
def get_list_product():
    return ProductController().get_list_product()
