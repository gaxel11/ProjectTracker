import peewee as pw
from app.models.task import Task


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""
    migrator.add_fields(Task,
                        color=pw.CharField(default="#FFFFFF",
                                           max_length=7,
                                           null=True))


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
    migrator.remove_fields(Task, "color")
