from flask import request, jsonify
from common.field_common import SECRET_KEY, PAGINATION
import jwt
from datetime import datetime
import uuid


class BaseController:

    @staticmethod
    def get_info_in_token(key):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return data.get(key)

    @staticmethod
    def validate_input(list_field, data_input):
        for i in list_field:
            if not data_input.get(i):
                return i

    @staticmethod
    def this_moment_create():
        dnow = datetime.now()
        return {
            'create_on': dnow,
            'update_on': dnow
        }

    @staticmethod
    def this_moment_update():
        return {
            'update_on': datetime.now()
        }

    @staticmethod
    def get_error(message):
        return {"error": message}

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid1())

    @staticmethod
    def get_info_paging_for_response(data, paging):
        if data.get(PAGINATION.TOTAL_PAGE):
            paging.update({
                PAGINATION.TOTAL_PAGE: data.get(PAGINATION.TOTAL_PAGE)
            })
        if data.get(PAGINATION.TOTAL_COUNT):
            paging.update({
                PAGINATION.TOTAL_COUNT: data.get(PAGINATION.TOTAL_COUNT)
            })
        if paging.get(PAGINATION.PAGE_PARAM) == -1:
            paging.pop(PAGINATION.PAGE_PARAM)
        return paging

    @staticmethod
    def generate_paging_from_args(args):
        paging = {
            PAGINATION.PAGE_PARAM: int(args.get(PAGINATION.PAGE_PARAM, PAGINATION.PAGE)),
            PAGINATION.PER_PAGE_PARAM: int(args.get(PAGINATION.PER_PAGE_PARAM, PAGINATION.PER_PAGE)),
        }
        return paging