-- Query to get latest exchange_rate for each month and currency

SELECT currency_name, exchange_rate, currency_code, exchange_date
FROM currency_rate
WHERE (currency_code, strftime('%Y-%m', exchange_date), exchange_date) IN (
    SELECT currency_code,
           strftime('%Y-%m', exchange_date) AS ym,
           MAX(exchange_date)
    FROM currency_rate
    GROUP BY currency_code, ym
)
ORDER BY currency_code, exchange_date DESC;


-- Query to get latest exchange_rate for each month and currency
-- BUT for cases, where today is not the latest day of the month, return update_at date instead of exchange_date

SELECT
    exchange_rate,
    currency_code,
    CASE
	/* if exchange_date contains current month but it's NOT the last day of the month ->
	use update_at, else use exchange_date */
	WHEN strftime('%m', exchange_date) == strftime('%m', CURRENT_DATE)
	AND NOT CURRENT_DATE = DATE('now', 'start of month', '+1 month', '-1 day')
        THEN update_at
        ELSE exchange_date
    END AS last_month_date
FROM currency_rate
WHERE (currency_code, strftime('%Y-%m', exchange_date), exchange_date, update_at) IN (
    SELECT
        currency_code,
        strftime('%Y-%m', exchange_date),
        MAX(exchange_date),
        update_at
    FROM currency_rate
    GROUP BY currency_code, strftime('%Y-%m', exchange_date)
)
ORDER BY currency_code, exchange_date DESC;

