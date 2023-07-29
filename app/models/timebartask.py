from .task import Task
from .timebar import TimeBar
from peewee import AutoField, DateTimeField, ForeignKeyField, Model
from config.database import database


class TimeBarTask(Model):
    id = AutoField(primary_key=True)
    timebar = ForeignKeyField(TimeBar, backref='tasks')
    task = ForeignKeyField(Task)
    start_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        database = database