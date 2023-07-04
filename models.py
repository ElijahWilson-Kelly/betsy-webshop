from peewee import *
import os

db = SqliteDatabase(os.path.join(os.getcwd(), "database.db"))



class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    address = CharField()
    # Billing Information
    credit_card_number = CharField()
    credit_card_expiry = DateField()
    credit_card_cvv = CharField()

class Tag(BaseModel):
    name = CharField(unique=True)

class Product(BaseModel):
    name = CharField()
    description = TextField() # Text Field used in case description is longer than 255 characters
    price_per_unit_cents = IntegerField()
    quantity = IntegerField()
    owned_by = ForeignKeyField(User, backref="products_owned")
    tags = ManyToManyField(Tag, backref="products")

class Transaction(BaseModel):
    product = ForeignKeyField(Product, backref="transactions")
    buyer = ForeignKeyField(User, backref="purchases")
    quantity = IntegerField()



ProductTag = Product.tags.get_through_model()

