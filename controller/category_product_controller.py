from controller.base_controller import BaseController
from model.mongo.category_product_model import CategoryProductModel
from flask import request, jsonify

class CategoryProductController(BaseController):

    def add_category(self):
        body = request.json
        name = body.get()
