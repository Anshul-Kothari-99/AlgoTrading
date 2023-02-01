# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 00:16:13 2023

@author: kotha
"""
import pandas as pd
'''
from os import walk
import csv

mypath="D:\\Python Scripts\\shares Analysis\\reserve\\"
files_list = next(walk(mypath), (None, None, []))[2] # this would extract all the files(shares) names present in the folder in a list

#print(files_list)

with open('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Historical Data Download\\YF_Ticker_Names.csv', 'w') as TempFile:
    # using csv.writer method from CSV package
    write = csv.writer(TempFile)      
    write.writerow(files_list)   
ticker_names = pd.read_csv('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Historical Data Download\\YF_Ticker_Names.csv', header=None).T
'''
ticker_names = pd.read_csv('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Historical Data Download\\NSE_Symbols.csv')

ticker_names['prefix'] = '.NS'
ticker_names.columns = ['Ticker_name', 'Prefix']
#ticker_names[['Ticker_name', 'delete']] = ticker_names['Ticker_name'].str.split('.', 1, expand=True)
#ticker_names.drop(['delete'], axis=1, inplace = True)
ticker_names['YF_Ticker_Name'] = ticker_names['Ticker_name'] + ticker_names['Prefix']
ticker_names.drop(['Ticker_name', 'Prefix'], axis=1, inplace = True)
#print(ticker_names)
#print(ticker_names.columns)

ticker_names.to_csv("YF_Ticker_Names.csv", index=False, header=False)
print('Done!!')
