from peewee import AutoField
from peewee import Model
from peewee import ForeignKeyField
from peewee import DateTimeField
from timebar import TimeBar
from task import Task
from config.database import database


class TimeBarTask(Model):
    id = AutoField(primary_key=True)
    timebar = ForeignKeyField(TimeBar, backref='tasks')
    task = ForeignKeyField(Task)
    start_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        database = database