from app.models.task import Task


def create_task(title, status,
                description=None, repository_url=None,
                page_url=None, time_elapsed=None):
    new_task = Task(
        title=title,
        description=description,
        status=status,
        repository_url=repository_url,
        page_url=page_url,
        time_elapsed=time_elapsed
    )
    new_task.save()
    
    
def update_task(id, **kwargs):
    try:
        task = Task.get_by_id(id)
    except Task.DoesNotExist:
        raise ValueError(f"La tarea con ID {id} no existe.")

    for field, value in kwargs.items():
        if value is not None:
            setattr(task, field, value)

    task.save()


def delete_task(id):
    try:
        task = Task.get_by_id(id)
    except Task.DoesNotExist:
        raise ValueError(f"La tarea con ID {id} no existe.")

    task.delete_instance()


