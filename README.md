# Fetching and Storing Gas Data

- Start/End dates, database login data, and sql queries can all be accessed in config.py
- createTables.py can be run to create the record and gas_data tables
- script.py can be used to fetch all the data between config.start_date and config.end_date

- Currently fetches from cycles 0 and 1 as through trying to access the data these were the only URLs that had data if there are some missing they can easily be added to the cycles list in script.py

-