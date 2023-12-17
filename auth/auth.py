from flask import jsonify, request
import jwt
from common.field_common import SECRET_KEY
from model.mongo.account_model import AccountModel, AccountField
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

            # decoding the payload to fetch the stored details
        data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        current_user = AccountModel().find({AccountField.id: data.get(AccountField.id)})
        if not current_user:
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated


def get_info_in_token(key):
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        # return 401 if token is not passed
    if not token:
        return jsonify({'message': 'Token is missing !!'}), 401

    data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    return data.get(key)
