import psycopg2


def connect_to_the_database():
    connection = psycopg2.connect(
        host="localhost",
        database="Project",
        user="postgres",
        password="admin",
        port="5432"
    )

    return connection
