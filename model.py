import os

from peewee import Model, CharField, DecimalField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class Donor(Model):
    name = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        database = db


class Donation(Model):
    value = DecimalField(decimal_places=2, auto_round=True)
    donor = ForeignKeyField(Donor, backref='donations')

    class Meta:
        database = db
