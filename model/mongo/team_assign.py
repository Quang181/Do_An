from model.mongo.base_mongo_model import BaseMongo, CONFIG_ACCOUNT_DB


class TeamAssignModel(BaseMongo):
    id_account = "id_account"
    id_team = "id_team"
    id = "id"
    position = "position"

    class Position:
        leader = "leader"
        member = "member"

    def __init__(self, col=None):
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["team_assign"]
