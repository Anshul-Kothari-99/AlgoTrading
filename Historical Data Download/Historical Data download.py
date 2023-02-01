# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:06:17 2023

@author: Anshul Kothari
"""

import yfinance as yf
from datetime import datetime, timedelta
import csv
import pandas as pd

Ticker_Names_file_path= ".\YF_Ticker_Names.csv"

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
    stock_data = yf.download(ticker[0], start = start_date, end = end_date, interval = timeframe)
    print('Ticker Name -------------> ', ticker[0])
    #print(stock_data.shape[0])
    if stock_data.shape[0] > 0:
        stock_data = stock_data.reset_index()
        stock_data['Date'] = pd.to_datetime(stock_data['Datetime']).dt.date
        stock_data['Time'] = pd.to_datetime(stock_data['Datetime']).dt.time
        stock_data.drop(['Datetime', 'Volume', 'Adj Close'], axis=1, inplace=True)
        print(stock_data.head())
        print('\n')
        #print(stock_data.columns)
    else:
        print('Download Failing for -------------> ', ticker[0], '\n')