### Currency rate script

*This repository contains*:
1. Task to get API currency code
2. SQLite DB `nbu_data.db`
3. Visualization for currency rates done in Tableau
4. SQL query and result
5. CSV file with db data

*Task is executed in next steps*:
1. Connect to NBU currency rates API (documentation https://bank.gov.ua/ua/open-data/api-dev point 1)
2. Get rates for certain period and certain currency codes
3. Load data to database (used SQLite)
4. Check if some dates are missing
5. Run API request for missing dates

To manually execute task open `task.py` and run it.
Example of logs after task run:
```
2025-04-17 20:48:05,670 - INFO - *** Saving data for currency code USD for 20250216 - 20250417
2025-04-17 20:48:05,674 - INFO - Inserted 61 lines into db
2025-04-17 20:48:05,817 - INFO - *** Saving data for currency code EUR for 20250216 - 20250417
2025-04-17 20:48:05,820 - INFO - Inserted 122 lines into db
2025-04-17 20:48:05,944 - INFO - *** Saving data for currency code GBP for 20250216 - 20250417
2025-04-17 20:48:05,948 - INFO - Inserted 183 lines into db
```
Install Db Browser for SQLite to check data

To run this task automatically in cloud:
- run by scheduling task as a cron job OR via schedule python lib on any cloud Linux server like EC2
- via AWS lambda to see task run status, logs, access to code etc.(better for monitoring & visibility)
- via Aiflow/Databricks to see task run status, logs, access to code etc. (better for monitoring & visibility)
