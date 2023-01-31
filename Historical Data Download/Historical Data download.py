# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:06:17 2023

@author: kotha
"""

import yfinance as yf
from datetime import datetime, timedelta
import csv

Ticker_Names_file_path= ".\\YF_Ticker_Names.csv"

with open(Ticker_Names_file_path, mode="r") as ticker_names:
    tickers = csv.reader(ticker_names)
    tickers = list(tickers)
#print(tickers)

n_days_ago = 59

today_date = datetime.now().date()
date_n_days_ago = today_date - timedelta(days = n_days_ago)
#print('Todays Date', today_date, date_n_days_ago)

start_date = date_n_days_ago
end_date = today_date
timeframe = '5m'

for ticker in tickers[:5]:
    data = yf.download(ticker[0], start = start_date, end = end_date, interval = timeframe)
    print(ticker[0])
    print(data.head())