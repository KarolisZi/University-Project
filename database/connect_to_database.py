import psycopg2
from values import constant


def connect_to_the_database():
    return psycopg2.connect(
        host="localhost",
        database="university_project",
        user="postgres",
        password="admin123",
        port="5432",
        options="-c search_path=dbo," + constant.SCHEMA
    )
