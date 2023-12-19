import datetime
import string

import jwt

from controller.base_controller import BaseController
from flask import request, jsonify
from common.field_common import ROLE, SECRET_KEY
import hashlib
import hmac
from common.config_common import get_redis
from model.mongo.account_model import AccountModel, AccountField
import uuid
import re
from model.mongo.lock_account import LockAccountModel
from model.mongo.history_lock_account import HistoryLockAccountModel
import random
from tools.string_tools import StringTool


class AccountController(BaseController):

    def create_account(self):
        if self.get_info_in_token(AccountField.role) != "admin":
            return jsonify(self.get_error("Bạn không có quyền tạo tài khoản"))

        body = request.json
        field_none = self.validate_input(AccountField.all_field, body)

        username = body.get(AccountField.username)
        password = body.get(AccountField.password)
        email = body.get(AccountField.email)
        fullname = body.get(AccountField.fullname)
        role = body.get(AccountField.role)
        phone = body.get(AccountField.phone)
        if field_none:
            return jsonify({"error": "{} not null".format(field_none)}), 413

        check_exits = AccountModel().find({AccountField.username: username})
        if check_exits:
            return jsonify({"error": "Username đã tồn tại"}), 413

        new_password = hmac.new(bytes(SECRET_KEY, "utf-8"), bytes(password, 'utf-8'), hashlib.sha256).hexdigest()
        id_account = self.generate_uuid()
        create_account = AccountModel(id=id_account, fullname=fullname, phone=phone, username=username,
                                      password=new_password, email=email,
                                      role=role).create_account(self.this_moment_create())
        if not create_account:
            return jsonify(self.get_error("Tạo tài khoản không thành công")), 413

        body.update({AccountField.id: id_account})
        return {
            "code": 200,
            "data": body
        }

    def update_account(self, account_id):
        body = request.json
        data_update = {}

        if self.get_info_in_token(AccountField.role) != "admin":
            return jsonify(self.get_error("Bạn không có quyền sửa tài khoản"))

        check_exits = AccountModel().find({AccountField.id: account_id})
        if not check_exits:
            return jsonify(self.get_error("Account id không tồn tại")), 413

        for i in [AccountField.password, AccountField.fullname, AccountField.phone]:
            if body.get(i) and i == AccountField.password:
                new_password = hmac.new(SECRET_KEY, body.get(i).encode('utf-8'), hashlib.sha256).hexdigest()
                data_update.update({i: new_password})
            elif body.get(i) and i == AccountField.phone:
                phone = self.chuan_hoa_so_dien_thoai(body.get(i))
                data_update.update({i: phone})
            elif body.get(i):
                data_update.update({i: body.get(i)})

        if data_update:
            data_update.update({**self.this_moment_create()})
            AccountModel().update_one({AccountField.id: account_id}, data_update)

        return {
            "code": 200,
            "data": data_update
        }

    def delete_account(self):
        if self.get_info_in_token(AccountField.role) != "admin":
            return jsonify(self.get_error("Bạn không có quyền xóa tài khoản"))

        body = request.json

        ids_account = body.get("ids_account")
        if self.get_info_in_token(AccountField.id) in ids_account:
            return jsonify(self.get_error("Bạn không được phép xóa tài khoản của chính mình"))

        if ids_account:
            check_exits = AccountModel().filter_one({AccountField.id: {"$in": ids_account}})

            if len(ids_account) != len(check_exits):
                return jsonify(self.get_error({"Account không tồn tại"})), 413

            delete_account = AccountModel().delete_many_data({AccountField.id: {"$in": ids_account}})
            if delete_account:
                return {
                    "code": 200
                }
        return jsonify(self.get_error("Xoác tài khoản thất bại"))

    @classmethod
    def chuan_hoa_so_dien_thoai(cls, so_dien_thoai):
        try:
            check_phone = re.match("^[0-9+]+", so_dien_thoai)
            if not check_phone:
                return so_dien_thoai
            so_dien_thoai = so_dien_thoai.replace("+", "")
            if so_dien_thoai.startswith('0') or so_dien_thoai.startswith('84'):
                return re.sub(r"^(0|84)([0-9]+)$", "+84\\2", so_dien_thoai)
            else:
                return re.sub(r"^([0-9]+)$", "+84\\1", so_dien_thoai)
        except Exception as err:
            print(err)
            return so_dien_thoai

    def login(self):
        body = request.json
        username = body.get(AccountField.username)
        password = body.get(AccountField.password)

        check_exits = AccountModel().filter_one({AccountField.username: username})
        if not check_exits:
            return jsonify(self.get_error("Tài khoản không tồn tại")), 413

        new_password = hmac.new(bytes(SECRET_KEY, 'utf-8'), password.encode('utf-8'), hashlib.sha256).hexdigest()
        check_lock = LockAccountModel().filter_one({LockAccountModel.account_id: check_exits.get(AccountField.id)})

        if check_lock.get(LockAccountModel.status) == "lock" and check_lock.get(
                LockAccountModel.time_login) > self.get_timestamp_now():
            return jsonify(self.get_error("Tài khoản bị khóa trong 1 phút vui lòng thử lại sau !"))

        if check_exits.get(AccountField.password) != new_password:
            if check_exits and check_lock.get(LockAccountModel.number_login, 0) >= 3:
                LockAccountModel().update_one({LockAccountModel.account_id: check_exits.get(AccountField.id)},
                                              {LockAccountModel.status: "lock",
                                               LockAccountModel.time_login: self.get_timestamp_now() + 60
                                               })

                HistoryLockAccountModel().insert_one({
                    LockAccountModel.account_id: check_exits.get(AccountField.id),
                    **self.this_moment_create()
                })
                return jsonify(self.get_error("Tài khoản của bạn bị khóa trong vòng 1 phút")), 413
            else:
                number_login_fail = check_lock.get(LockAccountModel.number_login, 0) + 1
                LockAccountModel().update_one({LockAccountModel.account_id: check_exits.get(AccountField.id)}, {
                    LockAccountModel.account_id: check_exits.get(AccountField.id),
                    LockAccountModel.number_login: number_login_fail,
                    LockAccountModel.time_login: self.get_timestamp_now(),
                    LockAccountModel.status: "active"
                }, True)

                return jsonify(self.get_error("Sai mật khẩu vui lòng thử lại")), 413

        if check_lock:
            LockAccountModel().delete_many_data({LockAccountModel.account_id: check_exits.get(AccountField.id)})

        self.set_account_online(check_exits.get(AccountField.id))
        token = self.create_jwt(check_exits)
        return {
            "code": 200,
            "role": check_exits.get(AccountField.role),
            "token": token
        }

    @classmethod
    def create_jwt(cls, data):
        data_encode = {
            AccountField.id: data.get(AccountField.id),
            AccountField.phone: data.get(AccountField.phone),
            AccountField.role: data.get(AccountField.role),
            AccountField.username: data.get(AccountField.username),
            AccountField.email: data.get(AccountField.email),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        jwt_token = jwt.encode(data_encode, SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def check_account_online(cls):
        r = get_redis()
        data_return = []
        account_online = r.lrange("account_onl", 0, -1)
        for i in account_online:
            data_return.append(i.decode('utf-8'))
        return data_return

    @classmethod
    def set_account_online(cls, account_id):
        r = get_redis()
        status = True
        account_onl = r.lrange('account_onl', 0, -1)
        for i in account_onl:
            if account_id == i.decode('utf-8'):
                status = False
        if status:
            r.rpush('account_onl', account_id)

    @staticmethod
    def get_timestamp_now():
        return datetime.datetime.timestamp(datetime.datetime.now())

    def forget_password(self):
        body = request.json
        username = body.get(AccountField.username)
        email = body.get(AccountField.email)

        check_exits = AccountModel().filter_one({AccountField.username: username})
        if not check_exits:
            return jsonify(self.get_error("Username không tồn tại")), 413

        email_db = check_exits.get(AccountField.email)

        if email != email_db:
            return jsonify(self.get_error("Email không hợp lệ")), 413

        random_str = self.generate_random_string(6)
        random_str = username + random_str

        r = get_redis()
        r.set(username, random_str, ex=180)

        # send_mail

        return {
            "code": 200,
            AccountField.username: username
        }

    def check_random_str(self):
        body = request.json
        password = body.get(AccountField.password)
        password_verify = body.get('password_verify')
        username = body.get(AccountField.username)
        code = body.get("code")

        for i in [AccountField.password, 'password_verify', AccountField.username, "code"]:
            if not body.get(i):
                return jsonify(self.get_error("{} không được để trống".format(i))), 413
        if password != password_verify:
            return jsonify(self.get_error("Mật khẩu mới và mật khẩu xác thức phải trùng nhau")), 413

        r = get_redis()
        check_code = r.get(username + code)
        if not check_code:
            return jsonify(self.get_error("Mã xác nhận không hợp lệ"))

        new_password = hmac.new(bytes(SECRET_KEY, "utf-8"), bytes(password, 'utf-8'), hashlib.sha256).hexdigest()
        AccountModel().update_one({AccountField.username: username}, {AccountField.password: new_password,
                                                                      **self.this_moment_update()})

        return {
            "code": 200
        }

    @classmethod
    def generate_random_string(cls, length):
        letters = string.ascii_letters + string.digits  # Ký tự bao gồm chữ cái và chữ số
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    def get_list_account(self):
        param = request.args

        paging = self.generate_paging_from_args(param)
        role_user = self.get_info_in_token(AccountField.role)
        role_user = "admin"
        role_user = self.get_list_permision(role_user)
        query = self.create_query_account(param, role_user)
        if not query:
            return {
                "data": [],
                "paging": {
                    "page": paging.get("page"),
                    "per_page": paging.get("per_page")
                }
            }

        list_data = AccountModel().get_list_entity(query, paging)
        paging = self.get_info_paging_for_response(list_data, paging)

        data_response = []
        for i in list_data.get("list_data"):
            id_account = i.get(AccountField.id)
            username = i.get(AccountField.username)
            phone = i.get(AccountField.phone)
            fullname = i.get(AccountField.fullname)
            role = i.get(AccountField.role)
            email = i.get(AccountField.email)

            data_account = {
                AccountField.id: id_account,
                AccountField.username: username,
                AccountField.phone: phone,
                AccountField.fullname: fullname,
                AccountField.role: role,
                AccountField.email: email
            }
            data_response.append(data_account)

        return {
            "code": 200,
            "data": data_response,
            "paging": paging
        }

    @staticmethod
    def get_list_permision(role):
        list_role = ["admin", "user", "client"]
        index = list_role.index(role)
        return list_role[index:]

    @staticmethod
    def status_account():
        return {
            "code": 200,
            "data": [
                {
                    "message": "Hoạt động",
                    "key": "onl"
                },
                {
                    "message": "Không hoạt động",
                    "key": "off"
                }
            ]
        }

    @staticmethod
    def get_role():
        return {
            "code": 200,
            "data": [
                {
                    "name": "Admin",
                    "key": "admin"
                },
                {
                    "name": "User",
                    "key": "user"
                },
                {
                    "name": "Client",
                    "key": "client"
                }
            ]
        }

    def create_query_account(self, param, role_user):
        name = param.get("name")
        status = param.get("status")
        role = param.get("role")

        data_query = []
        if name:
            data_query.append({"$or": [
                {AccountField.username: {"$regex": name,
                                         "$options": "i"}},
                {AccountField.fullname: {"$regex": name,
                                         "$options": "i"}}
            ]})

        if role:
            role = StringTool(role).separate_string_by_comma()
            role = list(set(role_user).intersection(role))
            if not role:
                return data_query

            data_query.append({AccountField.role: {"$in": role}})

        if status:
            account_onl = self.check_account_online()
            if status == "onl":
                data_query.append({AccountField.id: {"$in": account_onl}})

            elif status == "off":
                data_query.append({AccountField.id: {"$nin": account_onl}})

        if not data_query:
            return []

        return {"$and": data_query}

    def detail_account(self, account_id):
        if not account_id:
            return jsonify(self.get_error("Account id not null")), 413

        detail_account = AccountModel().filter_one({AccountField.id: account_id}, {"_id": 0})
        if not detail_account:
            return jsonify(self.get_error("Account_id not exits")), 413

        return {
            "code": 200,
            "data": detail_account
        }
    