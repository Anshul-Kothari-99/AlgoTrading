# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 00:16:13 2023

@author: kotha
"""
import pandas as pd

ticker_names = pd.read_csv('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Historical Data Download\\NSE_Symbols.csv')
ticker_names['prefix'] = '.NS'
ticker_names.columns = ['Ticker_name', 'Prefix']
#ticker_names[['Ticker_name', 'delete']] = ticker_names['Ticker_name'].str.split('.', 1, expand=True)
ticker_names['YF_Ticker_Name'] = ticker_names['Ticker_name'] + ticker_names['Prefix']
ticker_names.drop(['Ticker_name', 'Prefix'], axis=1, inplace = True)
#print(ticker_names)
#print(ticker_names.columns)

ticker_names.to_csv("YF_Ticker_Names.csv", index=False, header=False)
print('Done')