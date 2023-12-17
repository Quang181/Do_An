import re


class StringTool:
    patterns = {
        "[àáảãạăắằẵặẳâầấậẫẩ]": "a",
        "[đ]": "d",
        "[èéẻẽẹêềếểễệ]": "e",
        "[ìíỉĩị]": "i",
        "[òóỏõọôồốổỗộơờớởỡợ]": "o",
        "[ùúủũụưừứửữự]": "u",
        "[ỳýỷỹỵ]": "y",
    }

    def __init__(self, text=None):
        self.text = text

    def validate_email(self):
        if bool(re.match(r"[\w\.-]+@[\w\.-]+(?:\.[\w]+)+", self.text)):
            return True
        else:
            return False

    def separate_string_by_comma(self) -> list:
        if not self.text:
            return []
        return [element.strip() for element in self.text.split(',') if element.strip()]

    def utf8_to_ascii(self):
        if self.text is None:
            return ""
        output = self.text
        for regex, replace in self.patterns.items():
            output = re.sub(regex, replace, output)
            # deal with upper case
            output = re.sub(regex.upper(), replace.upper(), output)
        return output

    def convert_data_for_search_regex(self):
        text_search = self.utf8_to_ascii()
        result = re.sub(r"([\.\*\+\?\^\$\{\}\(\)\|\[\]])", r"\\\1", text_search)
        return result
