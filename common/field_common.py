import os


class ROLE:
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"
    USER = "USER"
    LIST_ROLE = [ADMIN, MANAGER, USER]


SECRET_KEY = os.getenv("SECRET_KEY")


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
    ACCOUNT_UPDATE = "/account/<account_id>"
    FORGET_PASSWORD = "/forget-password"
    CHANGE_PASSWORD = "/forget/change-password"
    LIST_ROLE = "/roles"
    LIST_STATUS = "/status"
    DETAIL_ACCOUNT = "/account/<account_id>"
    ACCOUNT_CLIENT = "/account/by_ids"
    ACCOUNT_CHECK_IN = "/account/check-in"
    GET_WAGE = "/account/get_wage"
    ACCOUNT_NOT_TEAM = "/account/not-team"


class CATEGORY:
    CATEGORYS = "/category"
    LIST_STATUS = "/category/status"


class TEAM:
    TEAM = "/team"
    TEAM_UPDATE = "/team/<team_id>"
    TEAM_ACCOUNT = "/team/account"


class METHOD:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"
