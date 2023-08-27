from peewee import (AutoField, CharField, IntegrityError, Model, TextField,
                    TimeField)
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
        
    @classmethod
    def create_task(cls, title, description, status, repository_url=None,
                    page_url=None, time_elapsed=None):
        try:
            task = cls.create(
                title=title,
                description=description,
                status=status,
                repository_url=repository_url,
                page_url=page_url,
                time_elapsed=time_elapsed
            )
            return task
        except IntegrityError as e:
            return None, str(e)
             
    @classmethod
    def update_task(cls, task_id, **kwargs):
        try:
            task = cls.get(cls.id == task_id)
            for key, value in kwargs.items():
                setattr(task, key, value)
            task.save()
            return task
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_task(cls, task_id):
        try:
            task = cls.get(cls.id == task_id)
            task.delete_instance()
            return True
        except cls.DoesNotExist:
            return False
        
    @classmethod
    def get_all_tasks(cls):
        tasks = cls.select()
        return tasks
    
    @classmethod
    def get_task_by_id(cls, task_id):
        try:
            task = cls.get(cls.id == task_id)
            return task
        except cls.DoesNotExist:
            return None

        


