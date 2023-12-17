from model.mongo.account_model import AccountModel
from model.mongo.lock_account import LockAccountModel

if __name__ == "__main__":
    AccountModel().sync_table()
    LockAccountModel().sync_table()
