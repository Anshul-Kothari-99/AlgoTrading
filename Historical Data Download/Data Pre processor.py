# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:55:47 2023

@author: kotha
"""
import pandas as pd
from os import walk
import datetime

mypath = "D:\\NSE_Stocks_5m_hist_data\\"
files_list = next(walk(mypath), (None, None, []))[2] # This would extract all the files(shares) names present in the folder

print(len(files_list))

for stock in files_list:
    testcases_file_path = mypath + stock    
    try:
        df = pd.read_csv(testcases_file_path)
        df['dt'] = df['Date'] + ' ' + df ['Time']
        df.rename(columns = {"Open":"open", "High":"high", "Low":"low", "Close":"close"},inplace=True)
        df.dt = pd.to_datetime(df.dt)
        df.drop(['Date', 'Time', 'Volume'], axis=1, inplace=True)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)    
    
        x = 0
        while df.iloc[x]['dt'].time() != datetime.time(9,15,0):
            x += 1
        df = df[x:]
        #print(df.shape)        
        df.to_csv(mypath + "pre processed data files\\" + stock[:-4] + ".csv", index=False)
    except:
        print("passed for ----->", stock[:-7])
        pass