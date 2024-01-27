import tushare as ts
import time
import os

def get_daily_data(token, ts_codes, start_date, end_date):
    """
    Fetches daily data for given ts_codes within the specified date range.

    Parameters:
    token (str): The token to access the Tushare Pro API.
    ts_codes (str): The ts_codes for which to fetch the data, separated by commas.
    start_date (str): The start date of the data in YYYYMMDD format.

    Returns:
    DataFrame: The fetched data.
    """
    pro = ts.pro_api(token)
    df = pro.daily(ts_code=ts_codes, start_date=start_date, end_date=end_date)
    return df

token = "8afb67c1647338eb997909599f974868a0e6837733e04e46cf1def4a"
ts_codes = '001217.SZ,603099.SH'

# Custom dates
date = input("Enter the start date in YYYYMMDD format: ")

while True:
    df = get_daily_data(token, ts_codes, date, date)
    print(df)
