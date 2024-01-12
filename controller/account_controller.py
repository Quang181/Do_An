import datetime
import string

import jwt

from controller.base_controller import BaseController
from flask import request, jsonify, make_response
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
from pymongo import DESCENDING
from model.mongo.check_in import CheckIn
from pymongo import InsertOne, UpdateOne
import calendar
from model.mongo.wage_account_model import WageAccountModel
from model.mongo.team_assign import TeamAssignModel
from common.date import Date
from model.mongo.calender_check_in import CalenderCheckIn


class AccountController(BaseController):

    def create_account(self):
        # if self.get_info_in_token(AccountField.role) != "admin":
        #     return jsonify(self.get_error("Bạn không có quyền tạo tài khoản"))

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

        for i in [AccountField.password, AccountField.fullname, AccountField.phone, AccountField.email, "verify_password", AccountField.role]:
            if body.get(i) and i == AccountField.password:

                if body.get(i) != body.get("verify_password"):
                    return jsonify(self.get_error("Password và Verify Password không được khác nhau")), 413

                new_password = hmac.new(bytes(SECRET_KEY, "utf-8"), bytes(body.get(i), 'utf-8'),
                                        hashlib.sha256).hexdigest()
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
        # if self.get_info_in_token(AccountField.role) != "admin":
        #     return jsonify(self.get_error("Bạn không có quyền xóa tài khoản"))

        body = request.json

        ids_account = body.get("ids_account")

        if not ids_account:
            return jsonify(self.get_error("Không được phép để trống tài khoản muốn xóa"))
        if self.get_info_in_token(AccountField.id) in ids_account:
            return jsonify(self.get_error("Bạn không được phép xóa tài khoản của chính mình"))

        if ids_account:
            check_exits = AccountModel().find({AccountField.id: {"$in": ids_account}})

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
            return jsonify(self.get_error("Tai khoan hoac mat khau khong ton tai")), 413


        new_password = hmac.new(bytes(SECRET_KEY, 'utf-8'), password.encode('utf-8'), hashlib.sha256).hexdigest()
        check_lock = LockAccountModel().filter_one({LockAccountModel.account_id: check_exits.get(AccountField.id)})

        if check_lock.get(LockAccountModel.status) == "lock" and check_lock.get(
                LockAccountModel.time_login) > self.get_timestamp_now():
            return jsonify(self.get_error("Tài khoản bị khóa trong 1 phút vui lòng thử lại sau !")), 413

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
        if not username:
            return jsonify(self.get_error("User name not null")), 413

        if not email:
            return jsonify(self.get_error("Email not null")), 413

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
        # if not query:
        #     return {
        #         "data": [],
        #         "paging": {
        #             "page": paging.get("page"),
        #             "per_page": paging.get("per_page")
        #         }
        #     }

        list_data = AccountModel().get_list_entity(query, paging, sort_options=[(AccountField.update_on, DESCENDING)])
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

        # if not data_query:
        #     return []
        if data_query:
            return {"$and": data_query}
        else:
            return {}

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

    def create_account_client(self):
        body = request.json
        username = body.get(AccountField.username)
        fullname = body.get(AccountField.fullname)
        email = body.get(AccountField.email)
        phone = body.get(AccountField.phone)
        password = body.get(AccountField.password)
        verify_password = body.get("verify_password")

        for i in [AccountField.username, AccountField.fullname, AccountField.email, AccountField.phone,
                  AccountField.password, "verify_password"]:
            if not body.get(i):
                return jsonify(self.get_error("{} Không được bỏ trống".format(i))), 413
        if password != verify_password:
            return jsonify(self.get_error("Mật khẩu và mật khẩu xác minh phải trùng nhau")), 413

        account_info = AccountModel().filter_one({AccountField.username: username})
        if account_info:
            return jsonify(self.get_error("Username đã tồn tại")), 413

        new_password = hmac.new(bytes(SECRET_KEY, "utf-8"), bytes(password, 'utf-8'), hashlib.sha256).hexdigest()
        id_account = self.generate_uuid()
        insert_account = AccountModel(id=id_account, username=username, email=email, fullname=fullname,
                                      password=new_password, role=AccountField.Role.client, phone=phone).create_account(
            self.this_moment_create())

        if not insert_account:
            return jsonify(self.get_error("Tạo tài khoản không thành công")), 413

        account_insert = AccountModel().filter_one({AccountField.username: username}, {"_id": 0})

        return {
            "code": 200,
            "data": account_insert
        }

    def get_info_account_by_ids(self):
        body = request.json
        ids = body.get("ids")

        if not ids:
            return jsonify(self.get_error("Ids không được để trống")), 413

        list_account = AccountModel().find({AccountField.id: {"$in": ids}}, {"_id": 0})
        return {
            "code": 200,
            "data": list_account
        }

    def check_in_account(self):
        body = request.json
        time = body.get("time")
        accounts = body.get("accounts")
        if not body:
            return jsonify(self.get_error("Body not null")), 413

        if not time:
            return jsonify(self.get_error("Time not null")), 413

        for i in accounts:
            if "account_id" not in i or "time_work" not in i:
                return jsonify(self.get_error("Validate error")), 413

        account_ids = [i.get("account_id") for i in accounts]
        check_exits = AccountModel().find({AccountField.id: {"$in": account_ids}})
        if len(account_ids) != len(check_exits):
            return jsonify(self.get_error("Account not exits")), 413

        time_first = self.set_time_to_first_time_in_day(Date.convert_str_to_date(time, "%d/%m/%Y"))
        if CheckIn().filter_one({CheckIn.time: time_first}):
            return jsonify(self.get_error("Đã check in ngày này ")), 413

        bulk_insert = []
        for i in accounts:
            account_id = i.get(CheckIn.account_id)
            time_work = i.get(CheckIn.time_work)

            data_insert = {
                CheckIn.account_id: account_id,
                CheckIn.time_work: time_work,
                CheckIn.time: time_first,
                **self.this_moment_create()
            }
            bulk_insert.append(InsertOne(data_insert))

        if bulk_insert:
            CheckIn().bulk_write(bulk_insert)

        CalenderCheckIn().insert_one({CalenderCheckIn.time: time_first,
                                      **self.this_moment_create()})

        return {
            "code": 200
        }

    def get_wage_account(self, account_id):
        # param = request.json
        # # account_id = param.get("account_id")
        time_now = datetime.datetime.now()
        month = time_now.month
        year = time_now.year
        convert_time_first_str = "{}-{}-{}".format(year, month, "01")
        time_first = datetime.datetime.strptime(convert_time_first_str, "%Y-%m-%d")
        time_first = time_first.timestamp()

        number_day = calendar.monthrange(year, month)[1]
        get_wage_account = WageAccountModel().filter_one({WageAccountModel.account_id: account_id})
        if not get_wage_account or not get_wage_account.get(WageAccountModel.wage):
            return {
                "code": 200,
                "data": {
                    "wage": 0,
                    "time_month": month,
                }
            }
        check_in = CheckIn().find({CheckIn.account_id: account_id,
                                   "$gte": time_first,
                                   "$lte": time_now.timestamp()})
        wage_by_day = get_wage_account.get(WageAccountModel.wage) / number_day
        total_wage = wage_by_day * len(check_in)

        return {
            "code": 200,
            "data": {
                "wage": total_wage,
                "time_month": month
            }
        }

    def account_not_in_team(self):
        check_account = TeamAssignModel().find({})
        if not check_account:
            list_account = AccountModel().find({AccountField.role: {"$ne": AccountField.Role.client}})
        else:
            account_ids = [i.get(TeamAssignModel.id_account) for i in check_account]
            list_account = AccountModel().find({AccountField.id: {"$nin": account_ids}})

        data_response = []
        for i in list_account:
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
            "data": data_response
        }

    @classmethod
    def set_time_to_first_time_in_day(cls, time):
        time_first = time.replace(hour=0, minute=0, second=0, microsecond=0)
        return time_first.timestamp()

    def check_day_check_in(self):
        body = request.args
        time = body.get("time")
        if not time:
            return jsonify(self.get_error("Time not null")), 413

        time_first = self.set_time_to_first_time_in_day(Date.convert_str_to_date(time, "%d/%m/%Y"))

        status = "no"
        if CalenderCheckIn().filter_one({CalenderCheckIn.time: time_first}):
            status = "yes"

        return {
            "code": 200,
            "status": status
        }

    def list_account_check_in_by_day(self):
        param = request.args
        time = param.get("time")
        if not time:
            return jsonify(self.get_error("Time not null")), 413

        time_first = self.set_time_to_first_time_in_day(Date.convert_str_to_date(time, "%d/%m/%Y"))

        list_checkin = CheckIn().find({CheckIn.time: time_first})

        time_work_convert = {}
        for i in list_checkin:
            id_account = i.get(CheckIn.account_id)
            time_work = i.get(CheckIn.time_work)

            time_work_convert.update({id_account: time_work})

        projection = {
            "_id": 0,
            AccountField.phone: 1,
            AccountField.username: 1,
            AccountField.fullname: 1,
            AccountField.email: 1,
            AccountField.role: 1,
            AccountField.id: 1
        }
        list_account = AccountModel().find({AccountField.role: {"$ne": AccountField.Role.client}}, projection=projection)
        for account in list_account:
            id_account = account.get(AccountField.id)
            account.update({"time_work": time_work_convert.get(id_account, 0)})

        return {
            "code": 200,
            "data": list_account
        }

    def list_account_not_client(self):
        projection = {
            "_id": 0,
            AccountField.phone: 1,
            AccountField.username: 1,
            AccountField.fullname: 1,
            AccountField.email: 1,
            AccountField.role: 1,
            AccountField.id: 1
        }
        list_account = AccountModel().find({AccountField.role: {"$ne": AccountField.Role.client}}, projection=projection)
        return {
            "code": 200,
            "data": list_account
        }
