import math
import os
import pymongo

from common.field_common import PAGINATION

MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_DB = os.environ.get("MONGO_DB")

Mongo_Client = pymongo.MongoClient(
    host="localhost", port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD)

CONFIG_ACCOUNT_DB = Mongo_Client[MONGO_DB]


class BaseMongo:
    def __init__(self, col=None) -> None:
        self.col = col

    def test(self):
        test = CONFIG_ACCOUNT_DB.get_collection("account")
        print(test)

    def filter_one(self, payload=None, projection=None):
        find_one = self.col.find_one(payload, projection)
        if not find_one:
            return {}
        return find_one

    def find(self, payload=None, skip=None, limit=None, projection=None):
        rs = self.col.find(payload, projection)
        if limit:
            rs = rs.limit(int(limit))
        if skip:
            rs = rs.skip(int(skip))
        return [x for x in rs if x] or []

    def insert_one(self, payload):
        try:
            self.col.insert_one(payload)
            return dict(payload)
        except Exception as error:
            raise error

    def update_one(self, query, payload, upsert=None):
        try:
            if upsert:
                self.col.update_one(query, {"$set": payload}, upsert=upsert)
            else:
                self.col.update_one(query, {"$set": payload})
            return dict(payload)
        except Exception as error:
            raise error

    def bulk_write(self, list_change: list):
        return self.col.bulk_write(list_change)

    def add_index(self, list_index: list, is_drop_index=False):
        if is_drop_index:
            self.col.drop_indexes()
        if not list_index:
            return
        self.col.create_indexes(list_index)

    def delete_many_data(self, query):
        return self.col.delete_many(query)

    @staticmethod
    def generate_limit_and_offset(paging):
        limit = paging.get(PAGINATION.PER_PAGE_PARAM)
        offset = (int(paging.get(PAGINATION.PAGE_PARAM)) - 1) * int(paging.get(PAGINATION.PER_PAGE_PARAM))
        return limit, offset

    def get_list_entity(self, search_options, paging, projection=None, sort_options=None,
                        select_fields: list = None):
        if select_fields and isinstance(select_fields, list):
            projection = self.generate_projection_from_select_fields(select_fields)

        cursor = self.col.find(search_options, projection)
        if sort_options:
            cursor.sort(sort_options)

        total_count = self.col.count_documents(search_options)
        total_page = 1
        if paging.get(PAGINATION.PAGE_PARAM) != -1:
            limit, offset = self.generate_limit_and_offset(paging)
            cursor.limit(limit).skip(offset)
            total_page = math.ceil(total_count / paging.get(PAGINATION.PER_PAGE_PARAM))

        list_data = list(cursor)
        results = {
            PAGINATION.LIST_DATA: list_data,
            PAGINATION.TOTAL_PAGE: total_page,
            PAGINATION.TOTAL_COUNT: total_count
        }
        return results

    def generate_projection_from_select_fields(self, select_fields):
        projection = {}
        for select_field in select_fields:
            projection.update({
                select_field: 1
            })
        projection.update({
            "_id": 0
        })
        return projection

if __name__ == "__main__":
    c = BaseMongo().test()