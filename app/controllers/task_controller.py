from datetime import timedelta
from app.models.task import Task
from config.loggers import logging
from app.models.constants import (
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_WAITING_FOR_CUSTOMER,
    TASK_STATUS_CLOSED,
    TASK_STATUS_RESOLVED,
    TASK_STATUS_SUSPENDED,
    TASK_STATUS_IN_TEST,
    TASK_STATUS_OPEN,
    TASK_STATUS_REOPENED,
)


class TaskController:

    @staticmethod
    def create_task(
            title,
            status,
            color="#FFFFFF",
            description=None,
            repository_url=None,
            page_url=None,
            time_passed=timedelta(hours=0),
    ):
        """Create a new task.

        Args:
        - title (str): Title of the task.
        - status (str): Status of the task. Must be one of the constants from constants.py.
        - color (str): Color of the task in hexadecimal format. Default is "#FFFFFF".
        - description (str, optional): Description of the task.
        - repository_url (str, optional): URL of the associated repository.
        - page_url (str, optional): URL of the associated page.
        - time_passed (timedelta): Time passed on the task. Default is 0 hours.

        Returns:
        - Task: The created task instance.
        """
        logging.debug("Attempting to create a new task...")
        valid_statuses = [
            TASK_STATUS_IN_PROGRESS,
            TASK_STATUS_WAITING_FOR_CUSTOMER,
            TASK_STATUS_CLOSED,
            TASK_STATUS_RESOLVED,
            TASK_STATUS_SUSPENDED,
            TASK_STATUS_IN_TEST,
            TASK_STATUS_OPEN,
            TASK_STATUS_REOPENED,
        ]
        if status not in valid_statuses:
            logging.error(f"Invalid status provided: {status}")
            raise ValueError(
                f"Invalid status. Must be one of {', '.join(valid_statuses)}.")

        task = Task.create(
            title=title,
            status=status,
            color=color,
            description=description,
            repository_url=repository_url,
            page_url=page_url,
            time_passed=time_passed,
        )
        logging.info(f"Task with ID {task.id} created successfully.")
        return task

    @staticmethod
    def edit_task(task_id, **kwargs):
        """Edit the fields of an existing task.

        Args:
        - task_id (int): ID of the task to be edited.
        - **kwargs: Fields to be updated with their new values.

        Returns:
        - Task: The edited task instance.
        """
        logging.debug(f"Attempting to edit task with ID {task_id}...")
        task = Task.get_by_id(task_id)
        for key, value in kwargs.items():
            setattr(task, key, value)
        task.save()
        logging.info(f"Task with ID {task_id} edited successfully.")
        return task

    @staticmethod
    def delete_task(task_id):
        """Delete a task by its ID.

        Args:
        - task_id (int): ID of the task to be deleted.

        Returns:
        - int: Number of rows deleted. Should be 1 if the task was found and deleted.
        """
        logging.debug(f"Attempting to delete task with ID {task_id}...")
        task = Task.get_by_id(task_id)
        rows_deleted = task.delete_instance()
        if rows_deleted == 1:
            logging.info(f"Task with ID {task_id} deleted successfully.")
        else:
            logging.warning(f"Task with ID {task_id} was not found.")
        return rows_deleted

    @staticmethod
    def add_time(task_id, hours):
        """Add hours to the time_elapsed field of a task.

        Args:
        - task_id (int): ID of the task.
        - hours (int): Number of hours to add.

        Returns:
        - Task: The updated task instance.
        """
        logging.debug(
            f"Attempting to add {hours} hours to task with ID {task_id}...")
        task = Task.get_by_id(task_id)
        adjustment = timedelta(hours=hours)
        task.adjust_time(adjustment)
        logging.info(
            f"Added {hours} hours to task with ID {task_id}. New time_elapsed: {task.time_elapsed}"
        )
        return task
