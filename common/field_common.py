import os


class ROLE:
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"
    USER = "USER"
    LIST_ROLE = [ADMIN, MANAGER, USER]


SECRET_KEY = "shoe_store"


class PAGINATION:
    PAGE = 1
    PER_PAGE = 15
    PAGE_PARAM = "page"
    PER_PAGE_PARAM = "per_page"
    SEARCH_TEXT = "search_text"
    TOTAL_PAGE = 'total_page'
    TOTAL_COUNT = 'total_count'
    LIST_DATA = "list_data"


class ACCOUNT:
    LOGIN = "/login"
    ACCOUNT = "/account"
    ACCOUNT_DELETE = "/account/delete"
    ACCOUNT_UPDATE = "/account/<account_id>"
    FORGET_PASSWORD = "/forget-password"
    CHANGE_PASSWORD = "/forget/change-password"
    LIST_ROLE = "/roles"
    LIST_STATUS = "/status"
    DETAIL_ACCOUNT = "/account/<account_id>"
    ACCOUNT_CLIENT = "/account/by_ids"
    CREATE_ACCOUNT_CLIENT = "/account/client"
    ACCOUNT_CHECK_IN = "/account/check-in"
    GET_WAGE = "/account/<account_id>/get_wage"
    ACCOUNT_NOT_TEAM = "/account/not-team"
    CHECK_DAY_CHECK_In = "/day/status-check-in"
    ACCOUNT_CHECK_IN_DAY = "/account/day/check-in"
    ACCOUNT_NOT_CLIENT = "/account/not-client"
    INFO_ACCOUNT = "/account/info"


class CATEGORY:
    CATEGORY = "/category"
    UPDATE_CATEGORY = "/category/<id_category>"
    LIST_STATUS = "/category/status"


class TEAM:
    TEAM = "/team"
    TEAM_UPDATE = "/team/<team_id>"
    TEAM_ACCOUNT = "/team/account"
    TEAM_DELETE = "/team/delete"


class METHOD:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"


class PRODUCT:
    PRODUCT = "/product"
    PRODUCT_UPDATE = "/product/<id_product>"
    PRE_ORDER = "/pre-order"
    CHECK_IN = "/check-in/<id_order>/room"
    CHECK_OUT = "/check-out/<id_order>/room"
    GET_PRICE_CHECK_OUT = "/check-out/get-price"
    STATUS_ORDER = "/status-order"
    ORDER = "/order"
    PRODUCT_VILA = "/product/vila"
    PRODUCT_NOT_VILA = "/product/not-vila"


class WAGE:
    WAGE = "/wage"
    WAGE_UPDATE = "/wage/<account_id>"


class WORK:
    WORK = "/work"
    WORK_UPDATE = "/work/<id_work>"
    WORK_USER = "/work-user"
    WORK_STAUT = "/work-status"
