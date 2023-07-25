from peewee import AutoField
from peewee import Model
from peewee import CharField
from peewee import TextField
from peewee import TimeField
from config.database import database


class Task(Model):
    id = AutoField(primary_key=True)
    title = CharField(max_length=255)
    description = TextField(null=True)
    status = CharField(max_length=50)
    repository_url = CharField(max_length=255, null=True)
    page_url = CharField(max_length=254, null=True)
    time_elapsed = TimeField(null=True)
    
    class Meta:
        database = database
