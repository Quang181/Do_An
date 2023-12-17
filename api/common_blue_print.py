from flask import Blueprint, Flask
from api.account import account

common_prefix = '/admin'

app = Flask(__name__)

app.register_blueprint(account, url_prefix=common_prefix)