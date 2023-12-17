from base_model import BaseModel
from peewee import CharField, IntegerField


class Product(BaseModel):
    id = CharField(36, primary_key=True)
    id_category = CharField(36)
    name = CharField(36)
    price = CharField(36)
    discount = CharField(36)
    source = CharField(36)
    status = IntegerField
    image_1 = CharField()
    image_2 = CharField()
    image_3 = CharField()
    image_4 = CharField()

    class Meta:
        table_name = "Product"