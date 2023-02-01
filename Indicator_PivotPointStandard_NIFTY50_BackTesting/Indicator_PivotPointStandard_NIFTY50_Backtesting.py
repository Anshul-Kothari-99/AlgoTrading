# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 23:45:15 2023

@author: Anshul Kothari
"""

import csv
import pandas as pd
import datetime
from os import walk

mypath = "D:\\NSE_Stocks_5m_hist_data\\"
files_list = next(walk(mypath), (None, None, []))[2] # this would extract all the files(shares) names present in the folder in a list

result_summary_for_NSE_stocks = []
failed_for =[]
count = 0

# HyperParameters - to be tunned
target_percentage_of_profit_for_call = 0.94  #0.94
target_percentage_of_sl_for_call = 0.495  #0.495

target_percentage_of_profit_for_put = 0.85   #0.85
target_percentage_of_sl_for_put = 0.535  #0.535 #0.54

for stock in files_list[:1]:
    testcases_file_path = mypath + stock
    testcases_file_path = "C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Indicator_PivotPointStandard_NIFTY50_BackTesting\\NIFTY 50_5minute.csv"
    count+=1
    
    try:
        with open(testcases_file_path, mode="r") as inputFile:
            inputReader = csv.DictReader(inputFile)
            
            df = pd.DataFrame(inputReader)    
            df['dt'] = df['Date'] + ' ' + df ['Time']
            df.rename(columns = {"Open":"open", "High":"high", "Low":"low", "Close":"close"},inplace=True)
            df.dt = pd.to_datetime(df.dt)
            df.drop(['Date', 'Time', 'Volume'], axis=1, inplace=True)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['open'] = df['open'].astype(float)    
            df = df[-20000:]    # Uncomment for NSE Analysis
            #print(df)
        
        result = []
        result_summary = []
        daysCount = 0
        x = 0
        
        while df.iloc[x]['dt'].time() != datetime.time(9,15,0):
            x += 1
        df = df[x:]
        
        # print(datetime.date(2015,2,16).weekday(), datetime.date(2015,2,16))
        # saturday - 5
        # sunday - 6
        # condition: df.iloc[i]["dt"].date().weekday() != 6 and df.iloc[i]["dt"].date().weekday() != 5
                
        resistance = -1
        intraday_call_close = []
        intraday_put_close = []
        call_target_hit = 0
        call_sl_hit = 0
        put_target_hit = 0
        put_sl_hit = 0
        support = 0
        entry_price = 0
        target_price = 0
        stoploss = 0
        
        next_day_support = -1
        next_day_resistance = -1
        count_no_trades = 0
        
        current_date = df.iloc[0]["dt"].date()
        call_target_hit_dates = []
        call_sl_hit_dates = []
        put_target_hit_dates = []
        put_sl_hit_dates = []
        
        high = 0
        low = 99999
        buy = 0
        sell = 0
        trade = 0
        trade_status = -1
        
        trade_status_encoding = {-1: 'No Trade Taken', 
                                 1:'Call - Buy', 
                                 2:'Call Target Hit', 
                                 3:'Call StopLoss Hit', 
                                 4:'IntraDay Timeout - Call Entry Closed', 
                                 11:'Put - Buy', 
                                 12:'Put Target Hit', 
                                 13:'Put StopLoss Hit', 
                                 14:'IntraDay Timeout - Put Entry Closed'}
        
        result.append(['Trade Date', 'Closing Price', 'Resistance', 'Support', 'Entry Price', 'StopLoss', 'Target Price', 'Trade Status'])
        
        for i in range(len(df)):
            if df.iloc[i]["dt"].date() == current_date:        
                if (resistance != -1):
                    # Check if resistance check is passed
                    resistance = next_day_resistance
                    support = next_day_support
                    
                    if (df.iloc[i]['close'] > resistance 
                    and trade == 0 and buy != 1 and sell != 1
                    and df.iloc[i]["dt"].time() != datetime.time(15,10,0) 
                    and df.iloc[i]["dt"].time() != datetime.time(15,5,0) 
                    and df.iloc[i]["dt"].time() != datetime.time(15,0,0)
                    and df.iloc[i]["dt"].time() != datetime.time(14,55,0)
                    ):
                        trade = 1
                        buy = 1
                        entry_price = df.iloc[i]['close']
                        target_price = entry_price * ((100+target_percentage_of_profit_for_call)/100)
                        stoploss = entry_price * ((100-target_percentage_of_sl_for_call)/100)
                        trade_status = 1
                        #print("Call - Buy")
                        
                    if buy == 1 and sell == 0 and trade == 1:
                        # Call Status Checks
                        if (df.iloc[i]['high'] > target_price):
                            sell = 1
                            trade = 0
                            call_target_hit = call_target_hit + 1
                            trade_status = 2
                            call_target_hit_dates.append(str(current_date))
                            #print("Call Target Hit")
                        if (df.iloc[i]['low'] < stoploss):
                            sell = 1
                            trade = 0
                            call_sl_hit = call_sl_hit + 1
                            trade_status = 3
                            call_sl_hit_dates.append(str(current_date))
                            #print("Call Stoploss Hit")                    
                            
                    if (df.iloc[i]['close'] < support 
                    and trade == 0 and buy != 1 and sell != 1
                    and df.iloc[i]["dt"].time() != datetime.time(15,10,0) 
                    and df.iloc[i]["dt"].time() != datetime.time(15,5,0) 
                    and df.iloc[i]["dt"].time() != datetime.time(15,0,0)
                    and df.iloc[i]["dt"].time() != datetime.time(14,55,0)
                    ):
                        sell = 1
                        trade = 1
                        entry_price = df.iloc[i]['close']
                        target_price = entry_price * ((100-target_percentage_of_profit_for_put)/100)
                        stoploss = entry_price * ((100+target_percentage_of_sl_for_put)/100)
                        trade_status = 11
                        #print("Put - Buy")
                    
                    if buy == 0 and sell == 1 and trade == 1:
                        # Put Status Check
                        if (df.iloc[i]['low'] < target_price):
                            buy = 1
                            trade = 0
                            put_target_hit = put_target_hit + 1
                            trade_status = 12
                            put_target_hit_dates.append(str(current_date))
                            #print("Put Target Hit")
                        if (df.iloc[i]['high'] > stoploss):
                            buy = 1
                            trade = 0
                            put_sl_hit = put_sl_hit + 1
                            trade_status = 13
                            put_sl_hit_dates.append(str(current_date))
                            #print("Put Stoploss Hit")
                        
                    if buy == 1 and sell == 0 and trade == 1 and df.iloc[i]["dt"].time() == datetime.time(15,10,0):
                        sell = 1
                        trade = 0
                        profit_percentage = (df.iloc[i]['close'] - entry_price)/entry_price
                        intraday_call_close.append(profit_percentage)
                        trade_status = 4
                        #print("IntraDay Timeout - Call Entry Closed")
                        
                        
                    if buy == 0 and sell == 1 and trade == 1 and df.iloc[i]["dt"].time() == datetime.time(15,10,0):
                        buy = 1
                        trade = 0
                        profit_percentage = (entry_price - df.iloc[i]['close'])/entry_price
                        intraday_put_close.append(profit_percentage)
                        trade_status = 14
                        #print("IntraDay Timeout - Put Entry Closed")
                
                if (df.iloc[i]["high"] > high):
                    high = df.iloc[i]["high"]          # Day high
                    #print('resistance_temp_high = ', high)
                if (df.iloc[i]["low"] < low):
                    low = df.iloc[i]["low"]            # Day low
                    #print('resistance_temp_low = ', low)
                
                if (df.iloc[i]["dt"].time() == datetime.time(15,25,0)):
                    close = df.iloc[i]["close"]
                    #print("Close Price recorded = ", close)
                    '''
                    result.append([current_date, 
                                   close, 
                                   resistance, 
                                   support, 
                                   entry_price, 
                                   stoploss, 
                                   target_price, 
                                   trade_status_encoding[trade_status]])
                    '''
                    
                    if trade_status == -1:
                        count_no_trades += 1
                        #print(trade_status_encoding[trade_status])
        
                    p = (high + low + close)/3
                    next_day_resistance = (p*2) - low
                    next_day_support = (p*2) - high
                    
                    high = 0
                    low = 99999
                    buy = 0
                    sell = 0
                    trade_status = -1
                    #print("Current Date :- ", current_date)
                    try:
                        current_date = df.iloc[i+1]["dt"].date()
                    except:
                        pass
                    daysCount += 1
                    #print('Day\'s Count = ', daysCount)
                    #print("\n")
                    
                    if resistance == -1:
                        #print("One/Fisrt Time Assignment")
                        resistance = next_day_resistance
                        support = next_day_support
        
        print('*********', count, ' - ' + stock + ' *********')
        '''      
        print("Count of Call Target Hits = ", call_target_hit)
        result_summary.append(["Count of Call Target Hits = ", call_target_hit])
        '''
        try:
            avg_call = sum(intraday_call_close)/len(intraday_call_close)*100
        except: 
            avg_call = 0  #Failed
            pass
        '''
        print("Count of Call closed for Intraday = ", len(intraday_call_close), "Avg % = ", avg_call)
        result_summary.append(["Count of Call closed for Intraday = ", len(intraday_call_close), "Avg % = ", avg_call])
        print("Count of Call StopLoss Hits = ", call_sl_hit)
        result_summary.append(["Count of Call StopLoss Hits = ", call_sl_hit])
        print("Count of Put Target Hits = ", put_target_hit)
        result_summary.append(["Count of Put Target Hits = ", put_target_hit])
        '''
        try:
            avg_put = sum(intraday_put_close)/len(intraday_put_close)*100 
        except: 
            avg_put = 0   #Failed
            pass
        '''
        print("Count of Put closed for Intraday = ", len(intraday_put_close), "Avg % = ", avg_put)
        result_summary.append(["Count of Put closed for Intraday = ", len(intraday_put_close), "Avg % = ", avg_put])
        print("Count of Put StopLoss Hits = ", put_sl_hit)
        result_summary.append(["Count of Put StopLoss Hits = ", put_sl_hit])
        
        print("\nTimes when No Trades were Taken = ", count_no_trades)
        result_summary.append(["Count of No Trades Taken = ", count_no_trades])
        '''
        
        '''
        print(type(len(intraday_call_close)))
        print(type(avg_call))
        print(type(call_target_hit))
        print(type(target_percentage_of_profit_for_call))
        print(type(call_sl_hit))
        print(type(target_percentage_of_sl_for_call))
        '''
        
        net_call = (len(intraday_call_close) * avg_call) + (call_target_hit * target_percentage_of_profit_for_call) - (call_sl_hit * target_percentage_of_sl_for_call)
        '''
        print("Net Call Returns = ", net_call)
        result_summary.append(["Net Call Returns = ", net_call])
        '''
        net_put = (len(intraday_put_close) * avg_put) + (put_target_hit * target_percentage_of_profit_for_put) - (put_sl_hit * target_percentage_of_sl_for_put)
        '''
        print("Net Put Returns = ", net_put)
        result_summary.append(["Net Put Returns = ", net_put])
        print("Net Returns = ", net_call + net_put)
        result_summary.append(["Net Results = ", net_call + net_put])
        '''
        
        '''
        print("\nDates on which Call Targets got Hit", call_target_hit_dates)
        print("\nDates on which Call SL got Hit", call_sl_hit_dates)
        print("\nDates on which Put Targets got Hit", put_target_hit_dates)
        print("\nDates on which Put SL got Hit", put_sl_hit_dates)
        '''
        
        result_summary_for_NSE_stocks.append([stock[:-7],
                                              call_target_hit, 
                                              len(intraday_call_close),
                                              avg_call,
                                              call_sl_hit,
                                              put_target_hit,
                                              len(intraday_put_close),
                                              avg_put,
                                              put_sl_hit,
                                              count_no_trades,
                                              net_call,
                                              net_put,
                                              net_call + net_put])
    
    except:
        failed_for.append(stock[:-7])
        print('\nAnalysis Failed for -------------> ', stock[:-7])
        pass


result_summary_for_NSE_stocks = pd.DataFrame(result_summary_for_NSE_stocks)
result_summary_for_NSE_stocks.columns = ["Stock Symbol",
                                         "Call Target Hits Count", 
                                         "Call closed for Intraday Count", 
                                         "Call Avg %",
                                         "Call StopLoss Hits Count", 
                                         "Put Target Hits Count", 
                                         "Put closed for Intraday Count", 
                                         "Put Avg %", 
                                         "Put StopLoss Hits Count", 
                                         "No Trades Taken Count", 
                                         "Net Call Returns", 
                                         "Net Put Returns",
                                         "Net Returns"]
print(result_summary_for_NSE_stocks)
result_summary_for_NSE_stocks.to_csv('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Indicator_PivotPointStandard_NIFTY50_BackTesting\\Stategy_Evaluation_on_Stocks.csv', index=False)

print('\nFailed for -------------> ', failed_for)

'''
with open('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Indicator_PivotPointStandard_NIFTY50_BackTesting\\Results.csv', 'w') as OutputFile:
    # using csv.writer method from CSV package
    write = csv.writer(OutputFile)      
    write.writerow(result[0])
    write.writerows(result[1:])
    write.writerows(result_summary)    
'''
print("\n*********************************************************************\n")
print("Report Generated Successfully!!!")