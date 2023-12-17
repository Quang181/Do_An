from model.base_model import BaseModel
from peewee import DateTimeField, CharField, IntegerField
from datetime import datetime
import uuid


class Team(BaseModel):
    id = CharField(36, primary_key=True)
    name = CharField(255)
    status = IntegerField()  # activate=1,not_activate=0, đang không sử dụng
    created_time = DateTimeField(default=datetime.now())
    updated_time = DateTimeField(default=datetime.now())
    created_by = CharField(36)
    updated_by = CharField(36)
    describe = CharField(255)
    module_name = CharField(36)

    class Meta:
        table_name = "Team"

    def create_team(self):
        return Team().create(id=uuid.uuid4(),
                             name=self.name,
                             status=1,
                             created_by=self.created_by,
                             updated_by=self.updated_by,
                             describe=self.describe,
                             module_name=self.module_name)

    @staticmethod
    def update_team(field_update):
        if field_update.get("name"):

        if field_update.get("describe"):

        if field_update.get("account_update"):

    @staticmethod
    def delete_team(id_team):
        return Team().delete().where(id=id_team)


    @staticmethod
    def get_list_team(search= None, category_team: list = None):
        query = Team.select()
        if search:
            query = query.where(Team.name.contains(search))
        if category_team:
            query = query.where(Team.module_name << category_team)

        return query
