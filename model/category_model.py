from base_model import BaseModel
from peewee import CharField, IntegerField


class CategoryProductModel(BaseModel):
    id = CharField(36, primary_key=True)
    name = CharField(36)
    status = IntegerField()

    class Meta:
        table_name = "Category"