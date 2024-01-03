import datetime


class Date:

    @staticmethod
    def convert_str_to_date(string, format="%Y-%m-%d"):
        date = datetime.datetime.strptime(string, format)
        return date
