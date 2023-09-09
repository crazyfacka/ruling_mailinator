import psycopg2
from psycopg2 import Error
from datetime import date

from confs import *

class Storage:
    def __init__(self):
        db_params = {
            'host': DB_HOST,
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD
        }

        try:
            self.connection = psycopg2.connect(**db_params)
            self.cursor = self.connection.cursor()
            self.__check_schema__()
        except Error as e:
            print("Error:", e)

    def __check_schema__(self):
        last_date_table = """CREATE TABLE IF NOT EXISTS last_date (
            id smallint UNIQUE,
            last_date date NOT NULL
        )"""

        parsed_messages_table = """CREATE TABLE IF NOT EXISTS parsed_messages (
            message_id bigint UNIQUE,
            message_date timestamptz NOT NULL
        )"""

        self.cursor.execute(last_date_table)
        self.cursor.execute(parsed_messages_table)
        self.connection.commit()

    def get_last_check_date(self):
        """Retrieves the last checked date from the DB"""
        query = "SELECT last_date FROM last_date WHERE id = 0"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            query = "INSERT INTO last_date (id, last_date) VALUES (%s, %s)"
            self.cursor.execute(query, (0, '2023-01-01'))
            self.connection.commit()
            return date(2023, 1, 1)

        return rows[0][0]

    def set_last_check_date(self, new_date):
        """Sets the last check date"""
        query = """INSERT INTO last_date (id, last_date) VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET last_date=%s WHERE last_date.id=%s"""
        self.cursor.execute(query, (0, new_date, new_date, 0))
        self.connection.commit()

    def close(self):
        """Closes the DB connection"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
