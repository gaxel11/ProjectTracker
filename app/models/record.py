from peewee import AutoField
from peewee import Model
from peewee import TextField
from peewee import TimeField
from peewee import ForeignKeyField
from peewee import DateTimeField
from .task import Task
from config.database import database


class Record(Model):
    id = AutoField(primary_key=True)
    task = ForeignKeyField(Task, backref="records")
    description = TextField(null=True)
    time_spent = TimeField()
    timestamp = DateTimeField()

    class Meta:
        database = database
