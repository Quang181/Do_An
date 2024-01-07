from api.common_blue_print import app
from flask_cors import CORS

CORS(app)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')

@app.before_request
def execute_before_request():
    """
    Thực thi trước khi xử lý request. Ví dụ: kết nối database.
    :return:
    """
    pass


@app.teardown_request
def execute_when(exec):
    """
    Thực thi khi một request bị ngắt. Ví dụ: ngắt kết nối database.
    :param exec:
    :return:
    """
    pass

if __name__ == '__main__':
    app = app
    app.run(host='0.0.0.0', port=5000, debug=True)
