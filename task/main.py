import sqlite3
from task_functions import get_currency_data, check_all_dates_loaded, db_name
from utils import create_table


def download_currency_exchange_data_task():
    """
    Get API currency exchange data and save it to db
    """
    with sqlite3.connect(db_name) as conn:
        # get API data
        get_currency_data(conn)

        # find missing dates
        missing_in_db_data = check_all_dates_loaded(conn)

        # get API data for specific dates
        for currency, date_list in missing_in_db_data.items():
            for date in date_list:
                get_currency_data(conn, currency=currency, date=date)


create_table()  # run only once to create table
download_currency_exchange_data_task()
