from api.common_blue_print import app

if __name__ == '__main__':
    app = app
    app.run(host='0.0.0.0', port=5000, debug=True)