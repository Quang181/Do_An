from controller.base_controller import BaseController
from flask import request, jsonify
from model.mongo.product_model import ProductModel
from model.mongo.category_product_model import CategoryProductModel


class ProductController(BaseController):

    def create_product(self):
        body = request.json
        name = body.get(ProductModel.name)
        id_category = body.get(ProductModel.id_category)
        price = body.get(ProductModel.price)
        image = body.get(ProductModel.image)
        account_id = self.get_info_in_token("id")

        if not CategoryProductModel().find({CategoryProductModel.id: id_category}):
            return jsonify(self.get_error("Loại sản phẩm không tồn tại ")), 413

        if ProductModel().filter_one({ProductModel.name: name}):
            return jsonify(self.get_error("Sản phẩm đã tồn tại")), 413

        product_id = self.generate_uuid()
        data_insert = {
            ProductModel.id: product_id,
            ProductModel.name: name,
            ProductModel.image: image,
            ProductModel.id_category: id_category,
            ProductModel.price: price,
            ProductModel.account_id: account_id
        }
        insert_data = ProductModel().insert_one(data_insert)

        if not insert_data:
            return jsonify(self.get_error("Thêm sản phẩm thất bại ")), 413

        return {
            "code": 200,
            "data": data_insert
        }

    def update_product(self):
        body = request.json

    def delete_product(self):
        pass

    def get_list_product(self):
        pass
