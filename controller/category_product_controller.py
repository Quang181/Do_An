from pymongo import DESCENDING

from controller.base_controller import BaseController
from model.mongo.category_product_model import CategoryProductModel
from flask import request, jsonify
import copy


class CategoryProductController(BaseController):

    def add_category(self):
        body = request.json
        name = body.get(CategoryProductModel.name)
        describe = body.get(CategoryProductModel.describe, "")

        if not name:
            return jsonify(self.get_error("Name not null")), 413

        check_name = CategoryProductModel().filter_one({CategoryProductModel.name: name})
        if check_name:
            return jsonify(self.get_error("Tên loại sản phẩm đã tồn tại")), 413

        id_category = self.generate_uuid()
        data_insert = {CategoryProductModel.id: id_category,
                       CategoryProductModel.name: name,
                       CategoryProductModel.describe: describe,
                       CategoryProductModel.status: "active",
                       **self.this_moment_create()}

        data_return = copy.deepcopy(data_insert)
        insert_category = CategoryProductModel().insert_one(data_insert)
        if not insert_category:
            return jsonify(self.get_error("Thêm loại sản phẩm thất bại")), 413

        return {
            "code": 200,
            "data": data_return
        }

    def update_category(self, id_category):
        body = request.json

        name = body.get(CategoryProductModel.name)
        describe = body.get(CategoryProductModel.describe)
        status = body.get(CategoryProductModel.status)

        check_exit = CategoryProductModel().filter_one({CategoryProductModel.id: id_category})
        if not check_exit:
            return jsonify(self.get_error("Loại sản phẩm không tồn tại ")), 413
        data_update = {}
        if name:
            data_update.update({CategoryProductModel.name: name})

        if describe:
            data_update.update({CategoryProductModel.describe: describe})

        if status:
            data_update.update({CategoryProductModel.status: status})

        if data_update:
            data_update.update({**self.this_moment_update()})
            CategoryProductModel().update_one({CategoryProductModel.id: id_category},
                                              data_update)
            return {
                "code": 200,
                "data": body
            }
        else:
            return jsonify(self.get_error("Data not null")), 413

    def delete_category(self):
        body = request.json
        ids_category = body.get("ids_category")
        check_exits = CategoryProductModel().find({CategoryProductModel.id: {"$in": ids_category}})
        if len(ids_category) != len(check_exits):
            return jsonify(self.get_error("Loại sản phẩm không tồn tại ")), 413

        delete_category = CategoryProductModel().delete_many_data({CategoryProductModel.id: {"$in": ids_category}})
        if not delete_category:
            return jsonify(self.get_error("Xóa thất bại ")), 413

        return {
            "code": 200
        }

    def list_category(self):
        param = request.args
        paging = self.generate_paging_from_args(param)
        status = param.get(CategoryProductModel.status)
        name = param.get("name")

        sort_options = [(CategoryProductModel.update_on, DESCENDING)]
        data_query = {}
        projection = {
            "_id": 0
        }
        if name:
            data_query.update({CategoryProductModel.name: {"$regex": name}})
        if status:
            data_query.update({CategoryProductModel.status: status})

        list_category = CategoryProductModel().get_list_entity(data_query, paging,projection=projection, sort_options=sort_options)
        paginated = self.get_info_paging_for_response(list_category, paging)

        return {
            "code": 200,
            "data": list_category,
            "paging": paginated
        }

    def list_status(self):
        data = [
            {
                "key": "active",
                "name": "Hoạt động",
            },
            {
                "key": "deactivate",
                "name": "Không hoạt động",
            }
        ]
        return {
            "code": 200,
            "data": data
        }
