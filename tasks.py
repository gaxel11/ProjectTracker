import time

from invoke import Collection, task
from peewee import OperationalError
from termcolor import colored

from app.models.record import Record
from app.models.task import Task
from app.models.timebar import TimeBar
from app.models.timebartask import TimeBarTask


@task
def install(c):
    if 'requirements.txt' in c.run('ls', hide=True).stdout.split():
        c.run('pip install -r requirements.txt')
        print("Dependencias instaladas.")
    else:
        print("No se encontró el archivo requirements.txt.")
        

@task
def lint(c):
    start_time = time.time()
    print("--------------Running 'lint' task--------------")
    print("Running 'pylint'...")
    results = c.run("pylint .", warn=True).stdout.strip().split("\n")
    for result in results:
        print(result)
    
    print("Running 'refurb'...")
    results = c.run("refurb .", warn=True).stdout.strip().split("\n")
    for result in results:
        print(result)
    
    print("Running 'flake8'...")
    results = c.run("flake8 .", warn=True).stdout.strip().split("\n")
    for result in results:
        print(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    if any(result.count(":") > 0 for result in results):
        message = (
            "Errors found. Review previous messages. "
            f"Elapsed time: {elapsed_time:.2f} seconds"
        )
        print(colored(message, "red"))
    else:
        message = (
            "The code is clean. "
            f"Elapsed time: {elapsed_time:.2f} seconds"
        )
        print(colored(message, "green"))

  
@task
def create_tables(c):
    table_classes = [Task, TimeBar, TimeBarTask, Record]
    if all(table.table_exists() for table in table_classes):
        print("Tables already exist.")
    else:
        try:
            for table in table_classes:
                table.create_table()
            print("Tables created successfully.")
        except OperationalError as e:
            print("Error creating tables:", str(e))


# Crear la colección principal
ns = Collection()
ns.add_task(install, "install")
ns.add_task(lint, "lint")
ns.add_task(create_tables, "create_tables")