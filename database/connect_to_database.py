import psycopg2
from values import constant


def connect_to_the_database():
    connection = psycopg2.connect(
        host="localhost",
        database="Project",
        user="postgres",
        password="admin",
        port="5432",
        options="-c search_path=dbo,"+constant.SCHEMA
    )

    return connection
