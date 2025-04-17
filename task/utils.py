import sqlite3

import pandas as pd

from task_functions import db_name


def create_table():
    """
    Helper function to run on db initialization. Run once when db is created.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency_rate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_name TEXT,
            exchange_rate REAL,
            currency_code TEXT,
            exchange_date DATE,
            update_at TIMESTAMP,
            UNIQUE(currency_code, exchange_date)
        )
        """)


def export_db_data_to_csv():
    """
    Helper function to export db data into csv file
    """
    with sqlite3.connect(db_name) as conn:
        df = pd.read_sql_query("SELECT * FROM currency_rate", conn)
        df.to_csv("currency_rate.csv", index=False)
