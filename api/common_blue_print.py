from flask import Blueprint, Flask
from api.account import account
from api.category_service import category
from api.team_service import team
from flask_cors import CORS
from api.product import product

common_prefix = '/admin'

app = Flask(__name__)
# CORS(app)
# app.config['content-type'] = 'application/json'

app.register_blueprint(account, url_prefix=common_prefix)
app.register_blueprint(category, url_prefix=common_prefix)
app.register_blueprint(team, url_prefix=common_prefix)
app.register_blueprint(product, url_prefix=common_prefix)