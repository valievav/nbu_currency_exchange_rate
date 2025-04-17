import requests
from datetime import datetime, timedelta
import sqlite3
from task_logging import logging

# main task params
db_name = 'nbu_data.db'
currency_list = ['USD', 'EUR', 'GBP']
start_date_str = '20250216'
end_date_str = datetime.today().strftime('%Y%m%d')
url = 'https://bank.gov.ua/NBU_Exchange/exchange_site'
# example url with params
# https://bank.gov.ua/NBU_Exchange/exchange_site?start=20250216&end=20250417&valcode=usd&sort=exchangedate&order=desc&json


def get_currency_data(db_conn: sqlite3.Connection, date: str = None, currency: str = None) -> None:
    """
    Extract API currency exchange data and save it to db
    """
    headers = {
        'Accept': 'application/json'
    }

    # use default currency list if currency is not provided
    currency_to_process = [currency] if currency else currency_list

    # get API data for each currency code
    for currency in currency_to_process:
        params = {'date': date} if date else {'start': start_date_str, 'end': end_date_str}
        params.update({'valcode': currency.lower(),
                   'sort': 'exchangedate',
                   'order': 'desc',
                   'json': ''})

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if not data:
            logging.error(f'Currency {currency} - no data found')
            return

        # save data to db
        date_val = date if date else f'{start_date_str} - {end_date_str}'
        logging.info(f'*** Saving data for currency code {currency} for {date_val}')
        save_data(data, db_conn)


def save_data(data: dict, db_conn: sqlite3.Connection) -> None:
    """
    Save data to db
    """
    with db_conn:
        values = []

        for line in data:
            values.append(
                (line['enname'], line['rate'], line['cc'],
                 datetime.strptime(line['exchangedate'], '%d.%m.%Y'), datetime.now())
            )

        db_conn.executemany('INSERT OR REPLACE INTO currency_rate '
                            '(currency_name, exchange_rate, currency_code, exchange_date, update_at) '
                            'VALUES (?, ?, ?, ?, ?)', values)
        rows_inserted = db_conn.total_changes
        logging.info(f'Inserted {rows_inserted} lines into db')


def check_all_dates_loaded(db_conn: sqlite3.Connection) -> dict:
    """
    Check that there no missing values for dates
    """
    with db_conn:
        # response format [('USD', '2025-04-17 00:00:00'), ('USD', '2025-04-16 00:00:00'), ...]
        res = db_conn.execute('SELECT DISTINCT currency_code, exchange_date FROM currency_rate').fetchall()

    existing_data = {currency: [] for currency in currency_list}
    for (currency, date) in res:
        if currency not in existing_data:
            logging.error(f'Unknown currency {currency} in db')
        existing_data[currency].append(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime('%Y%m%d'))

    start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
    end_date = datetime.strptime(end_date_str, "%Y%m%d").date()

    expected_dates = [
        (start_date + timedelta(days=i)).strftime('%Y%m%d')
        for i in range((end_date - start_date).days + 1)
    ]

    missing_in_db_data = {currency: [] for currency in currency_list}
    for currency in currency_list:
        # get dates that are missing in db - need to retry to get data for these dates from API if it exists
        missing_in_db = set(expected_dates) - set(existing_data[currency])
        if missing_in_db:
            logging.error(f'Currency {currency} - Found missing dates in db - {missing_in_db}')
            missing_in_db_data[currency] = list(missing_in_db)

        # get dates that are out of the expected range (we should not have such cases at all)
        # need to investigate them to find root cause
        # (either API sent data for invalid dates OR issue in our expected_dates)
        extra_in_db = set(existing_data[currency]) - set(expected_dates)
        if extra_in_db:
            logging.error(f'Currency {currency} - Found extra dates in db - {extra_in_db}')

    return missing_in_db_data
