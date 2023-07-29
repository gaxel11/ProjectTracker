from peewee import AutoField, DateTimeField, Model
from config.database import database


class TimeBar(Model):
    id = AutoField(primary_key=True)
    start_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        database = database