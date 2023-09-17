import datetime
from app.models.task import Task
from playhouse.postgres_ext import IntervalField


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""
    migrator.add_fields(Task,
                        time_passed=IntervalField(
                            default=datetime.timedelta(hours=0), null=True))


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
    migrator.remove_fields(Task, "time_passed")
