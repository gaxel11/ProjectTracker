import os
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
    # Obtener todos los archivos Python en el directorio actual
    python_files = [f for f in os.listdir() if f.endswith(".py")]
    
    start_time = time.time()
    print("--------------Running 'lint' task--------------")
    
    # Imprimir los archivos que se van a revisar
    print("Files to be checked:", ", ".join(python_files))
    
    print("Running 'pylint'...")
    pylint_exit_code = c.run("pylint .", warn=True).return_code
    
    print("Running 'refurb'...")
    refurb_exit_code = c.run("refurb .", warn=True).return_code
    
    print("Running 'flake8'...")
    flake8_exit_code = c.run("flake8 .", warn=True).return_code

    end_time = time.time()
    elapsed_time = end_time - start_time

    if any([pylint_exit_code, refurb_exit_code, flake8_exit_code]):
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
    start_time = time.time()
    table_classes = [Task, TimeBar, TimeBarTask, Record]
    if all(table.table_exists() for table in table_classes):
        print("Tables already exist.")
    else:
        try:
            for table in table_classes:
                print(f"Creating table {table.__name__}...")
                table.create_table()
            end_time = time.time()
            elapsed_time = end_time - start_time
            message = (
                "Tables created successfully. "
                f"Elapsed time: {elapsed_time:.2f} seconds"
            )
            print(colored(message, "green"))
        except OperationalError as e:
            end_time = time.time()
            elapsed_time = end_time - start_time
            message = (
                f"Error creating tables: {e}. "
                f"Elapsed time: {elapsed_time:.2f} seconds"
            )
            print(colored(message, "red"))
            

# Crear la colección principal
ns = Collection()
ns.add_task(install, "install")
ns.add_task(lint, "lint")
ns.add_task(create_tables, "create_tables")