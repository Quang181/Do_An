import copy
import datetime

from pymongo import DESCENDING

from controller.base_controller import BaseController
from flask import request, jsonify
from model.mongo.product_model import ProductModel
from model.mongo.category_product_model import CategoryProductModel
from tools.string_tools import StringTool
from common.date import Date
from model.mongo.check_in_product import CheckInProduct


class ProductController(BaseController):

    def create_product(self):
        body = request.form
        name = body.get(ProductModel.name)
        id_category = body.get(ProductModel.id_category)
        price = body.get(ProductModel.price)
        image = request.files.get("image")
        account_id = self.get_info_in_token("id")
        # account_id = "0885d4a6-af07-11ee-8f5a-5559e80602f2"
        for i in [ProductModel.name, ProductModel.id_category, ProductModel.price]:
            if not body.get(i):
                return jsonify(self.get_error("{} not null".format(i))), 413

        if not CategoryProductModel().find({CategoryProductModel.id: id_category}):
            return jsonify(self.get_error("Loại sản phẩm không tồn tại ")), 413
        pwd = "/opt/deploy/shoe-store"
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
        data_return = copy.deepcopy(data_insert)
        insert_data = ProductModel().insert_one(data_insert)

        if not insert_data:
            return jsonify(self.get_error("Thêm sản phẩm thất bại ")), 413

        return {
            "code": 200,
            "data": data_return
        }

    def update_product(self, id_product):
        body = request.form
        data_update = {}
        for i in [ProductModel.name, ProductModel.image, ProductModel.id_category, ProductModel.price]:
            data_update.update({i: body.get(i)}) if body.get(i) else ""

        if not ProductModel().find({ProductModel.id: id_product}):
            return jsonify(self.get_error("id product không tồn tại ")), 413

        if body.get(ProductModel.id_category) and not CategoryProductModel().find(
                {CategoryProductModel.id: body.get(ProductModel.id_category)}):
            return jsonify(self.get_error("id category khong ton tai")), 413

        if data_update:
            update_data = ProductModel().update_one({ProductModel.id: id_product}, data_update)
            if update_data:
                return {
                    "code": 200,
                    "data": data_update
                }
            else:
                return jsonify(self.get_error("Update san pham that bai"))
        return {
            "code": 200,
            "data": data_update
        }

    def delete_product(self):
        body = request.json
        ids_product = body.get("ids_product")
        if not ids_product:
            return jsonify(self.get_error("ID product not null")), 413
        delete_product = ProductModel().delete_many_data({ProductModel.id: {"$in": ids_product}})
        return {
            "code": 200
        }

    def get_list_product(self):
        param = request.args
        name = param.get(ProductModel.name)
        ids_category = param.get("ids_category")
        paging = self.generate_paging_from_args(param)

        query = {}
        if name:
            query.update({ProductModel.name: {"$regex": name}})
        if ids_category:
            ids_category = StringTool(ids_category).separate_string_by_comma()
            query.update({ProductModel.id_category: {"$in": ids_category}})
        sort_options = [(CategoryProductModel.update_on, DESCENDING)]
        list_data = ProductModel().get_list_entity(query, paging, {"_id": 0}, sort_options)
        paginated = self.get_info_paging_for_response(list_data, paging)

        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    def get_list_vila(self):
        param = request.args
        paging = self.generate_paging_from_args(param)
        sort_options = [(CategoryProductModel.update_on, DESCENDING)]
        list_data = ProductModel().get_list_entity({ProductModel.name: "Vila"}, paging, {"_id": 0}, sort_options)
        paginated = self.get_info_paging_for_response(list_data.get("list_data"), paging)
        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    def get_list_product_not_vila(self):
        param = request.args
        paging = self.generate_paging_from_args(param)
        sort_options = [(CategoryProductModel.update_on, DESCENDING)]
        list_data = ProductModel().get_list_entity({ProductModel.name: {"$nin": ["Vila"]}}, paging, {"_id": 0},
                                                   sort_options)
        paginated = self.get_info_paging_for_response(list_data.get("list_data"), paging)
        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    def check_in_vila(self):
        body = request.json

        cccd = body.get("cccd")
        name = body.get("name")
        phone = body.get("phone")
        email = body.get("email")
        id_product = body.get("id_product")
        status = body.get("status")
        time_check_in = body.get(CheckInProduct.time_check_in)
        time_check_out = body.get(CheckInProduct.time_check_out)

        if not status:
            return jsonify(self.get_error("status not null")), 413

        if status != CheckInProduct.Status.pre_order:
            return jsonify(self.get_error("Status khong hop le")), 413

        for i in [CheckInProduct.cccd, CheckInProduct.name, CheckInProduct.phone, CheckInProduct.email,
                  CheckInProduct.id_product, CheckInProduct.time_check_in, CheckInProduct.time_check_out]:
            if not body.get(i):
                return jsonify(self.get_error("{} not null".format(i))), 413

        check_exits = ProductModel().filter_one({ProductModel.id: id_product})
        if not check_exits:
            return jsonify(self.get_error("id product not exits")), 413

        check_exits_category = CategoryProductModel().filter_one(
            {CategoryProductModel.id: check_exits.get(ProductModel.id_category),
             CategoryProductModel.name: "Vila"})
        if not check_exits_category:
            return jsonify(self.get_error("Product not Vila")), 413
        time_check_in = Date.convert_str_to_date(time_check_in, "%d/%m/%Y:%H:%M:%S")
        time_check_out = Date.convert_str_to_date(time_check_out, "%d/%m/%Y:%H:%M:%S")

        check_exits = CheckInProduct().filter_one({CheckInProduct.id_product: id_product,
                                                   CheckInProduct.status: {"$ne": CheckInProduct.Status.check_out},
                                                   "$or": [
                                                       {CheckInProduct.time_check_in: {"$lte": time_check_in},
                                                        CheckInProduct.time_check_out: {"$gte": time_check_out}},
                                                       {
                                                           CheckInProduct.time_check_in: {"$lte": time_check_out},
                                                           CheckInProduct.time_check_out: {"$gte": time_check_out}
                                                       }
                                                   ]})
        if check_exits:
            return jsonify(self.get_error("Phòng đã có khách hàng đặt trước trong khoảng thời gian đó")), 413
        return {
            "code": 200
        }
        
    def set_str_to_date(self, date):
        date = date.replace(hour=12, minute=0, second=0, microsecond=0)
        return date

    def status_product(self):
        data_return = [
            {
                "key": "pre_order",
                "name": "Đặt trước"
            },
            {
                "key": "check_in",
                "name": "Lấy phòng",
            },
            {
                "key": "check_out",
                "name": " Trả phòng"
            }
        ]
        return {
            "code": 200,
            "data": data_return
        }
