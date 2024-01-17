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
from model.mongo.account_model import AccountModel, AccountField
import os
from werkzeug.utils import secure_filename
import math


class ProductController(BaseController):

    def create_product(self):
        body = request.form
        name = body.get(ProductModel.name)
        id_category = body.get(ProductModel.id_category)
        price = body.get(ProductModel.price)
        image = request.files.get("image")
        # account_id = self.get_info_in_token("id")
        # account_id = "0885d4a6-af07-11ee-8f5a-5559e80602f2"
        for i in [ProductModel.name, ProductModel.id_category, ProductModel.price]:
            if not body.get(i):
                return jsonify(self.get_error("{} not null".format(i))), 413

        if image:
            url_file = os.path.dirname(__file__)
            # url_file = url_file + "image"
            # if "controller" in url_file:
            url_file = url_file.split("controller")
            url_file = url_file[0] + "image"
            filename = secure_filename(image.filename)
            image.save(os.path.join(url_file, filename))
            # "http://52.63.96.9:5000"
            # image = "http://52.63.96.9:5000" + url_file + "/" + filename
            # image = "http://52.63.96.9:5000" + url_file + "/" + filename
            image = url_file + "/" + filename

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
            # ProductModel.account_id: account_id
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
        data = CategoryProductModel().filter_one({CategoryProductModel.name: "Vila"})
        if not data:
            return {
                "code": 200,
                "data": [],
                "paging": paging
            }
        list_data = ProductModel().get_list_entity({ProductModel.id_category: data.get(CategoryProductModel.id)},
                                                   paging, {"_id": 0}, sort_options)
        paginated = self.get_info_paging_for_response(list_data, paging)
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
        paginated = self.get_info_paging_for_response(list_data, paging)
        return {
            "code": 200,
            "data": list_data.get("list_data"),
            "paging": paginated
        }

    # def check_in_vila(self):
    #     body = request.json
    #
    #     cccd = body.get("cccd")
    #     name = body.get("name")
    #     phone = body.get("phone")
    #     email = body.get("email")
    #     id_product = body.get("id_product")
    #     status = body.get("status")
    #     time_check_in = body.get(CheckInProduct.time_check_in)
    #     time_check_out = body.get(CheckInProduct.time_check_out)
    #
    #     if not status:
    #         return jsonify(self.get_error("status not null")), 413
    #
    #     if status != CheckInProduct.Status.pre_order:
    #         return jsonify(self.get_error("Status khong hop le")), 413
    #
    #     for i in [CheckInProduct.cccd, CheckInProduct.name, CheckInProduct.phone, CheckInProduct.email,
    #               CheckInProduct.id_product, CheckInProduct.time_check_in, CheckInProduct.time_check_out]:
    #         if not body.get(i):
    #             return jsonify(self.get_error("{} not null".format(i))), 413
    #
    #     check_exits = ProductModel().filter_one({ProductModel.id: id_product})
    #     if not check_exits:
    #         return jsonify(self.get_error("id product not exits")), 413
    #
    #     check_exits_category = CategoryProductModel().filter_one(
    #         {CategoryProductModel.id: check_exits.get(ProductModel.id_category),
    #          CategoryProductModel.name: "Vila"})
    #     if not check_exits_category:
    #         return jsonify(self.get_error("Product not Vila")), 413
    #     time_check_in = Date.convert_str_to_date(time_check_in, "%d/%m/%Y:%H:%M:%S")
    #     time_check_out = Date.convert_str_to_date(time_check_out, "%d/%m/%Y:%H:%M:%S")
    #
    #     check_exits = CheckInProduct().filter_one({CheckInProduct.id_product: id_product,
    #                                                CheckInProduct.status: {"$ne": CheckInProduct.Status.check_out},
    #                                                "$or": [
    #                                                    {CheckInProduct.time_check_in: {"$lte": time_check_in},
    #                                                     CheckInProduct.time_check_out: {"$gte": time_check_out}},
    #                                                    {
    #                                                        CheckInProduct.time_check_in: {"$lte": time_check_out},
    #                                                        CheckInProduct.time_check_out: {"$gte": time_check_out}
    #                                                    }
    #                                                ]})
    #     if check_exits:
    #         return jsonify(self.get_error("Phòng đã có khách hàng đặt trước trong khoảng thời gian đó")), 413
    #     return {
    #         "code": 200
    #     }
    #
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

    def pre_order(self):
        body = request.json
        start = body.get("start")
        end = body.get("end")
        id_product = body.get("id_product")
        id_account = body.get("id_account")

        for i in ["start", "end", "id_product", "id_account"]:
            if not body.get(i):
                return jsonify(self.get_error("{} not null".format(i))), 413

        if not ProductModel().filter_one({ProductModel.id: id_product}):
            return jsonify(self.get_error("San pham khong ton tai")), 413
        start = Date.convert_str_to_date(start, "%d/%m/%Y")
        end = Date.convert_str_to_date(end, "%d/%m/%Y")
        start = Date.convert_date_to_timestamp(start)
        end = Date.convert_date_to_timestamp(end)
        if not AccountModel().filter_one({AccountField.id: id_account}):
            return jsonify(self.get_error("Account note exits")), 413

        if CheckInProduct().filter_one({"$or": [
            {CheckInProduct.time_check_in: {"$lte": start},
             CheckInProduct.time_check_out: {"$gte": start}},
            {CheckInProduct.time_check_in: {"$lte": end},
             CheckInProduct.time_check_out: {"$gte": end}}]}):
            return jsonify(self.get_error("Phòng đã có người đặt trước đó ")), 413
        id_orderr = self.generate_uuid()
        data_iinsert = {
            CheckInProduct.id: id_orderr,
            CheckInProduct.id_product: id_product,
            CheckInProduct.status: CheckInProduct.Status.pre_order,
            CheckInProduct.time_check_in: start,
            CheckInProduct.time_check_out: end,
            CheckInProduct.id_account: id_account,
            "total_price": 0,
            **self.this_moment_create()
        }
        data_return = copy.deepcopy(data_iinsert)
        insert = CheckInProduct().insert_one(data_iinsert)

        return {
            "code": 200,
            "data": data_return
        }

    def check_in(self, id_order):
        check_exit = CheckInProduct().filter_one({CheckInProduct.id: id_order})

        if not check_exit:
            return jsonify(self.get_error("ID khong ton tai")), 413

        CheckInProduct().update_one({CheckInProduct.id: id_order},
                                    {CheckInProduct.status: CheckInProduct.Status.check_in,
                                     **self.this_moment_update()})

        data_return = CheckInProduct().filter_one({CheckInProduct.id: id_order}, {"_id": 0})
        return {
            "code": 200,
            "data": data_return
        }

    def get_price_check_out(self):
        body = request.json
        time = body.get("time")
        id_product = body.get("id_product")
        id_account = body.get("id_account")
        id_order = body.get("id_order")
        product = body.get("product", [])
        list_product = [i.get("id_product") for i in product]
        list_product.append(id_product)
        if not id_order:
            return jsonify(self.get_error("id_order not null")), 413

        check_exist = ProductModel().find({ProductModel.id: {"$in": list_product}})
        if len(list_product) != len(check_exist):
            return jsonify(self.get_error("ID product not exits")), 413

        check_exits_account = AccountModel().filter_one({AccountField.id: id_account})
        if not check_exits_account:
            return jsonify(self.get_error("Account not exits")), 413

        info_check_in = CheckInProduct().filter_one({CheckInProduct.id: id_order})
        if not info_check_in:
            return jsonify(self.get_error("Order not exist")), 413

        get_price_by_product = {}
        for i in check_exist:
            product_id = i.get(ProductModel.id)
            price = i.get(ProductModel.price)

            get_price_by_product.update({product_id: price})

        total_price = 0
        for i in product:
            id_product_order = i.get("id_product")
            number = i.get("number")

            price = int(get_price_by_product.get(id_product_order, 0))

            price = price * number
            total_price = total_price + price

        price_room = get_price_by_product.get(id_product)
        time_check_in = info_check_in.get(CheckInProduct.time_check_in)
        tim_check_out = info_check_in.get(CheckInProduct.time_check_out)
        time = Date.convert_str_to_date(time, "%d/%m/%Y")
        time = Date.convert_date_to_timestamp(time)

        if time > tim_check_out:
            price_by_day = (time - time_check_in) // 86400
            price_by_day = price_by_day * int(price_room)
        else:
            price_by_day = (tim_check_out - time_check_in) // 86400
            price_by_day = price_by_day * int(price_room)
        total_price = total_price + price_by_day
        return {
            "code": 200,
            "total_price": total_price
        }

    def list_order(self):
        params = request.args
        paging = self.generate_paging_from_args(params)
        name_room = params.get("name")
        status = params.get("status")
        start = params.get("start")
        end = params.get("end")

        data_query = {}
        if status:
            status = StringTool(status).separate_string_by_comma()
            data_query.update({CheckInProduct.status: {"$in": status}})
        if name_room:
            data_query.update({CheckInProduct.name: name_room})
        if start and end:
            start = Date.convert_str_to_date(start, "%d/%m/%Y")
            end = Date.convert_str_to_date(end, "%d/%m/%Y")
            start = Date.convert_date_to_timestamp(start)
            end = Date.convert_date_to_timestamp(end)

            data_query.update({
                CheckInProduct.time_check_in: {"$gte": start},
                CheckInProduct.time_check_out: {"$lte": end}
            })
        sort_options = [(CategoryProductModel.update_on, DESCENDING)]
        list_check_in = CheckInProduct().get_list_entity(data_query, paging, {"_id": 0}, sort_options)
        paginated = self.get_info_paging_for_response(list_check_in, paging)
        ids_account = []
        ids_product = []
        convert_product = {}
        convert_category = {}
        for i in list_check_in.get("list_data"):
            ids_account.append(i.get(CheckInProduct.id_account))
            ids_product.append(i.get(CheckInProduct.id_product))

        if ids_product:
            list_product = ProductModel().find({ProductModel.id: {"$in": ids_product}},
                                               projection={"_id": 0, ProductModel.id_category: 1,
                                                           ProductModel.name: 1,
                                                           ProductModel.id: 1})
            ids_category = []
            for i in list_product:
                convert_product.update({i.get(ProductModel.id): i})
                ids_category.append(i.get(ProductModel.id_category))

            if ids_category:
                list_category = CategoryProductModel().find({CategoryProductModel.id: {"$in": ids_category}},
                                                            projection={"_id": 0,
                                                                        CategoryProductModel.id: 1,
                                                                        CategoryProductModel.name: 1})
                for i in list_category:
                    convert_category.update({i.get(CategoryProductModel.id): i})

        data_account = {}
        if ids_account:
            list_account = AccountModel().find({AccountField.id: {"$in": ids_account}}, projection={"_id": 0,
                                                                                                    AccountField.id: 1,
                                                                                                    AccountField.username: 1,
                                                                                                    AccountField.fullname: 1,
                                                                                                    AccountField.email: 1,
                                                                                                    AccountField.phone: 1,
                                                                                                    AccountField.role: 1})
            for i in list_account:
                id_account = i.get(AccountField.id)
                data_account.update({id_account: i})
        for order in list_check_in.get("list_data"):
            id_product = order.get(CheckInProduct.id_product)
            id_account = order.get(CheckInProduct.id_account)
            info_account = data_account.get(id_account, {})
            check_in = datetime.datetime.fromtimestamp(order.get(CheckInProduct.time_check_in))
            check_out = datetime.datetime.fromtimestamp(order.get(CheckInProduct.time_check_out))
            order.update({"info_account": info_account,
                          CheckInProduct.time_check_in: check_in,
                          CheckInProduct.time_check_out: check_out})
            order.update({"info_product": convert_product.get(id_product, {})})
            order.update({"info_category": convert_category.get(
                convert_product.get(id_product, {}).get(ProductModel.id_category))})

        return {
            "code": 200,
            "data": list_check_in.get("list_data"),
            "paging": paginated
        }

    def status_order(self):
        list_return = [
            {
                "key": CheckInProduct.Status.pre_order,
                "name": "Đặt phòng"
            },
            {
                "key": CheckInProduct.Status.check_in,
                "name": "Check in"
            },
            {
                "key": CheckInProduct.Status.check_out,
                "name": "Check out"
            }
        ]
        return {
            "code": 200,
            "data": list_return
        }

    def check_out(self, id_order):
        body = request.json
        total_price = body.get("total_price")
        if not total_price:
            return jsonify(self.get_error("Total price not null")), 413
        if not CheckInProduct().filter_one({CheckInProduct.id: id_order}):
            return jsonify(self.get_error("Hoa don khong ton tai")), 413

        update_order = CheckInProduct().update_one({CheckInProduct.id: id_order},
                                                   {"total_price": total_price,
                                                    "status": CheckInProduct.Status.check_out})

        return {
            "code": 200,
        }



