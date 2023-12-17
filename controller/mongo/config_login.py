from controller.base_controller import BaseController
from model.mongo.config_login import ConfigLogin
from flask import request, jsonify
from common.config_common import get_redis


class ConfigLoginController(BaseController):

    def create_config_login(self):
        body = request.json

        if not body:
            return jsonify({"error": "Config login not null"})

        username = body.get("username")
        password = body.get("password")
        other = body.get("other")

        regex_user_name = ""
        regex_pass_word = ""
        if username:
            regex_user_name = self.create_regex_user_name(username)
        if password:
            regex_pass_word = self.create_regex_user_name(password)

        r = get_redis()
        if regex_user_name:
            r.set(self.create_key_config("username"), regex_user_name)
        if regex_pass_word:
            r.set(self.create_key_config("password"), regex_pass_word)
        if other:
            r.set(self.create_key_config("other"), other)
        create_config = ConfigLogin().insert_data(body)
        if create_config:
            return {"data": body}
        else:
            return jsonify({"error": "Not create config login"}), 500

    @classmethod
    def create_regex_user_name(cls, data):
        min_us = data.get("min")
        max_us = data.get("max")
        char = data.get("character")
        number = data.get("number")

        regex_user_name = ""
        if number:
            regex_user_name += "(?=.*[a-z])(?=.*[0-9]{%s,})" % int(number)
        if char:
            regex_user_name += "(?=.*[a-z])(?=.*[-_.@]{%s,})" % int(char)
        regex_user_name += "[-_.@a-z0-9]"
        len_str = ""
        if min_us and max_us:

            len_str = "{{}, {}}".format(int(min_us), int(max_us))
        elif min_us:
            len_str = "{{},}".format(int(min_us))
        else:
            len_str = "{1, {}}".format(int(max_us))
        regex_return = ""
        regex_return += regex_user_name if regex_user_name else ""
        regex_return += len_str if len_str else ""

        return "^(" + regex_return + ")$"

    @classmethod
    def create_key_config(cls, text: str):
        return "{}_config".format(text)
