from invoke import task, Collection
from termcolor import colored


@task
def install(c):
    if 'requirements.txt' in c.run('ls', hide=True).stdout.split():
        c.run('pip install -r requirements.txt')
        print("Dependencias instaladas.")
    else:
        print("No se encontró el archivo requirements.txt.")


@task
def lint(c):
    print("--------------Ejecutando la tarea 'lint'--------------")
    print("Ejecutando 'pylint'...")
    results = c.run("pylint .", warn=True).stdout.strip().split("\n")
    for result in results:
        print(result)
    
    print("Ejecutando 'refurb'...")
    results = c.run("refurb .", warn=True).stdout.strip().split("\n")
    for result in results:
        print(result)
    
    print("Ejecutando 'flake8'...")
    results = c.run("flake8 .", warn=True).stdout.strip().split("\n")
    for result in results:
        print(result)

    if any(result.count(":") > 0 for result in results):
        print(colored("Errors found. Review previous messages.", "red"))
    else:
        print(colored("The code is clean", "green"))
    print("--------------La tarea 'lint' se ha completado---------------")
  

# Crear la colección principal
ns = Collection()
ns.add_task(install, "install")
ns.add_task(lint, "lint")
