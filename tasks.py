import importlib
import os
import time

from itertools import permutations

from invoke import Collection, task
from peewee import Model
from peewee_migrate import Router
from termcolor import colored
from colorama import Style

from config.database import database
from config.loggers import logging
from config.loggers import LoggingSetup


@task
def install(c, debug=False):
    LoggingSetup.setup_logging(debug)
    logging.info(Style.BRIGHT + "Running install: " + Style.RESET_ALL)
    logging.info("Starting dependency installation...")
    try:
        result = c.run("ls", hide=True)
        if "requirements.txt" in result.stdout.split():
            with open("requirements.txt", "r") as file:
                dependencies = [line.strip() for line in file.readlines()]
                for dependency in dependencies:
                    if dependency and not dependency.startswith(
                            "#"):  # Skip comments and empty lines
                        logging.info(f"Installing dependency: {dependency}")
            c.run("pip install -r requirements.txt")
            logging.info(
                colored("Dependencies successfully installed.", "green"))
        else:
            logging.warning("requirements.txt file not found.")
    except Exception as e:
        logging.error(f"An error occurred during installation: {e}")


@task
def lint(c, debug=False):
    # Setup logging based on the provided flag
    LoggingSetup.setup_logging(debug)

    start_time = time.time()

    logging.info(Style.BRIGHT + "Running lint task..." + Style.RESET_ALL)

    # Fetch all the Python files in the current directory
    python_files = [
        os.path.join(root, file) for root, _, files in os.walk(".")
        for file in files if file.endswith(".py")
    ]

    # Display files to be checked
    logging.info("Files to be checked: %s", ", ".join(python_files))

    # Run formatters first to attempt auto-fixing
    for formatter, command in (
        ("autopep8", "autopep8 --in-place --recursive ."),
        ("black", "black ."),
        ("yapf", "yapf --in-place --recursive ."),
    ):
        logging.info(Style.BRIGHT + f"Running formatter '{formatter}'..." +
                     Style.RESET_ALL)
        c.run(command, warn=True)
        logging.info(Style.BRIGHT + f"'{formatter}' finished formatting." +
                     Style.RESET_ALL)

    # Now, run linters to detect remaining issues
    linters = {
        "pylint": "pylint .",
        "refurb": "refurb .",  # Assuming 'refurb' is another linting tool
        "flake8": "flake8 .",
    }

    issues_detected = False

    for linter, command in linters.items():
        logging.info(Style.BRIGHT + f"Running linter '{linter}'..." +
                     Style.RESET_ALL)
        exit_code = c.run(command, warn=True).return_code
        if exit_code:
            logging.warning(f"{linter} found issues.")
            issues_detected = True

    end_time = time.time()
    elapsed_time = end_time - start_time

    if issues_detected:
        message = ("Code smells detected. Please review the above messages. "
                   f"Elapsed time: {elapsed_time:.2f} seconds")
        logging.error(message)
    else:
        message = f"The code is clean. Elapsed time: {elapsed_time:.2f} seconds"
        logging.info(colored(message, "green"))


@task
def init_database(c, debug=False):
    LoggingSetup.setup_logging(debug)
    logging.info(Style.BRIGHT + "Running init-db: " + Style.RESET_ALL)

    error_message = "Database initialization failed."

    logging.info("Starting database initialization...")

    start_time = time.time()

    try:
        create_tables()
        run_migrations()
        logging.info(
            colored("Database initialization completed successfully.",
                    "green"))
    except Exception as e:
        logging.error(f"{e}.")
        logging.error(error_message)

    end_time = time.time()

    elapsed_time = end_time - start_time
    logging.info(f"Elapsed time: {elapsed_time:.2f} seconds")


def run_migrations():
    logging.info(Style.BRIGHT + "Running run_migrations: " + Style.RESET_ALL)

    router = Router(database, migrate_dir="./app/models/migrations")
    applied_migrations = []

    pending_migrations = router.diff
    if not pending_migrations:
        logging.info("No pending migrations to apply.")
    else:
        logging.info("Applying pending migrations...")
        for migration in pending_migrations:
            try:
                logging.debug(f"Applying migration: {migration}.")
                router.run(migration)
                applied_migrations.append(migration)
                logging.info(f"Successfully applied migration: {migration}.")
            except Exception as e:
                logging.error(
                    f"Error applying migration {migration}: {e}. Rolling back..."
                )
                for applied_migration in reversed(applied_migrations):
                    try:
                        router.run(applied_migration)
                        logging.warning(
                            f"Reverted migration: {applied_migration}.")
                    except Exception as rollback_error:
                        rollback_error_msg = f"Error reverting migration {applied_migration}: {rollback_error}"
                        logging.critical(rollback_error_msg)
                raise e


def create_tables():
    table_classes = fetch_all_table_classes()
    logging.info(Style.BRIGHT + "Running create_all_tables: " +
                Style.RESET_ALL)
    logging.debug(f"Found {len(table_classes)} table classes.")

    if all(table.table_exists() for table in table_classes):
        logging.info("Tables already exist.")
        return

    all_possible_orders = list(permutations(table_classes))
    globally_created_tables = set()
    pending_tables = list(table_classes)

    for order in all_possible_orders:
        order = [table for table in order if table in pending_tables]
        for table in order:
            try:
                logging.info(f"Attempting to create table {table.__name__}...")
                table.create_table()
                globally_created_tables.add(table)
                pending_tables.remove(table)
            except Exception as e:
                logging.debug({e})
                logging.info(
                    f"Table {Style.BRIGHT}{table.__name__}{Style.RESET_ALL} pending creation"
                )

        logging.debug(
            f"Pending tables are: {[t.__name__ for t in pending_tables]}")

        if not pending_tables:
            logging.info("All tables created successfully.")
            break

    if pending_tables:
        logging.warning("Rolling back due to unresolved dependencies.")
        for table in reversed(list(globally_created_tables)):
            try:
                table.drop_table()
                logging.debug(f"Successfully dropped table {table.__name__}")
            except Exception as e:
                logging.error(f"Exception when dropping {table.__name__}: {e}")
                logging.critical(
                    f"Critical failure while attempting rollback of table {table.__name__}."
                )

        raise Exception(f"Could not resolve dependencies for tables: "
                        f"{[t.__name__ for t in pending_tables]}")


def fetch_all_table_classes():
    logging.info(Style.BRIGHT + "Running fetch_all_table_classes: " +
                 Style.RESET_ALL)
    models_dir = "./app/models"
    logging.debug(f"Fetching model files from directory: {models_dir}")

    model_files = [
        f[:-3] for f in os.listdir(models_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]

    logging.debug(f"Found {len(model_files)} model files.")

    table_classes_set = set()

    for model_file in model_files:
        module = importlib.import_module(f"app.models.{model_file}")
        logging.debug(f"Imported module: app.models.{model_file}")

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr,
                                                     Model) and attr != Model:
                table_classes_set.add(attr)
                logging.debug(
                    f"Added table class {attr_name} from {model_file}")

    logging.info(f"Total of {len(table_classes_set)} table classes fetched.")

    return list(table_classes_set)


# Crear la colección principal
ns = Collection()
ns.add_task(install, "install")
ns.add_task(lint, "lint")
ns.add_task(init_database, "init_db")
