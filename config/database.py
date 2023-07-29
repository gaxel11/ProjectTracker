from peewee import PostgresqlDatabase

db_config = {
    'host': 'localhost',
    'port': 5433,
    'dbname': 'PTdb',
    'user': 'tad',
    'password': 'tad'
}

database = PostgresqlDatabase(db_config['dbname'],
                              user=db_config['user'],
                              password=db_config['password'],
                              host=db_config['host'],
                              port=db_config['port'])