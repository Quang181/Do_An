from model.base_model import BaseModel
from peewee import CharField


class TeamAssign(BaseModel):
    id = CharField(36, primary_key=True)
    team_id = CharField(36)
    account_id = CharField(36)
    permission = CharField(255)

    class Meta:
        table_name = "TeamAssign"
