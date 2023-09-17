import datetime
from peewee import AutoField, CharField, Model, TextField
from config.database import database
from playhouse.postgres_ext import IntervalField


class Task(Model):
    id = AutoField(primary_key=True)
    title = CharField(max_length=255)
    description = TextField(null=True)
    status = CharField(max_length=50)
    repository_url = CharField(max_length=255, null=True)
    page_url = CharField(max_length=254, null=True)
    time_elapsed = IntervalField(null=True)
    time_passed = IntervalField(default=datetime.timedelta(hours=0), null=True)

    class Meta:
        database = database

    def adjust_time(self, adjustment, subtract=False):
        """
        Adjust the time_passed field of the Task model.

        Args:
        - adjustment (datetime.timedelta): Amount of time to adjust.
        - subtract (bool, optional): If True, subtracts the time. Default is False to add time.
        """
        if not isinstance(adjustment, datetime.timedelta):
            raise ValueError("adjustment should be of type datetime.timedelta")

        if subtract:
            self.time_passed -= adjustment
        else:
            self.time_passed += adjustment

        self.save()  # Persist the change to the database.
