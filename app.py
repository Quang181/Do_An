from api.common_blue_print import app
from flask_cors import CORS

CORS(app)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')


if __name__ == '__main__':
    app = app
    app.run(host='0.0.0.0', port=5000, debug=True)
