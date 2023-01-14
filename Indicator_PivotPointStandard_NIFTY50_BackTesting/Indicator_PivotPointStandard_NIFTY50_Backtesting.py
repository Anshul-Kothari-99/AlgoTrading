# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 23:45:15 2023

@author: Anshul Kothari
"""

import csv
import pandas as pd
import datetime

testcases_file_path= "C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Indicator_PivotPointStandard_NIFTY50_BackTesting\\NIFTY 50_15minute.csv"

with open(testcases_file_path, mode="r") as inputFile:
    inputReader = csv.DictReader(inputFile)
    
    df = pd.DataFrame(inputReader)    
    df['temp'] = df['Date'] + ' ' + df ['Time']
    df.rename(columns = {"temp":"dt", "Open":"open", "High":"high", "Low":"low", "Close":"close"},inplace=True)
    df.dt = pd.to_datetime(df.dt)
    df.drop(['Date', 'Time', 'Volume'], axis=1, inplace=True)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)    
    df = df[-5000:]
    #print(df.head())
    #print(df.shape)

result = []
result_summary = []
daysCount = 0
x = 0

while df.iloc[x]['dt'].time() != datetime.time(9,15,0):
    x+=1

df = df[x:]
#print(df.head())

#print(datetime.date(2015,2,16).weekday(), datetime.date(2015,2,16))
# saturday - 5
# sunday - 6
#condition: df.iloc[i]["dt"].date().weekday() != 6 and df.iloc[i]["dt"].date().weekday() != 5


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

current_date = df.iloc[0]["dt"].date()

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
            #print("resistance if-check passed")
            resistance = next_day_resistance
            support = next_day_support
            
            if df.iloc[i]['close'] > resistance and trade == 0 and df.iloc[i]["dt"].time() != datetime.time(15,15,0) and buy != 1 and sell != 1:
                trade = 1
                buy = 1
                entry_price = df.iloc[i]['close']
                target_price = entry_price * 1.008
                stoploss = entry_price * 0.996
                trade_status = 1
                print("Call - Buy")
                
            if buy == 1 and sell == 0 and trade == 1:
                #print("Call status checks")
                if (df.iloc[i]['high'] > target_price):
                    sell = 1
                    trade = 0
                    call_target_hit = call_target_hit + 1
                    trade_status = 2
                    print("Call Target Hit")
                if (df.iloc[i]['low'] < stoploss):
                    sell = 1
                    trade = 0
                    call_sl_hit = call_sl_hit + 1
                    trade_status = 3
                    print("Call Stoploss Hit")
                    
                    
            if df.iloc[i]['close'] < support and trade == 0 and df.iloc[i]["dt"].time() != datetime.time(15,15,0)  and buy != 1 and sell != 1:
                sell = 1
                trade = 1
                entry_price = df.iloc[i]['close']
                target_price = entry_price * 0.992
                stoploss = entry_price * 1.004
                trade_status = 11
                print("Put - Buy")
            
            if buy == 0 and sell == 1 and trade == 1:
                #print("put status check")
                if (df.iloc[i]['low'] < target_price):
                    buy = 1
                    trade = 0
                    put_target_hit = put_target_hit + 1
                    trade_status = 12
                    print("Put Target Hit")
                if (df.iloc[i]['high'] > stoploss):
                    buy = 1
                    trade = 0
                    put_sl_hit = put_sl_hit + 1
                    trade_status = 13
                    print("Put Stoploss Hit")
                    
                
            if buy == 1 and sell == 0 and trade == 1 and df.iloc[i]["dt"].time() == datetime.time(15,0,0):
                sell = 1
                trade = 0
                profit_percentage = (df.iloc[i]['close'] - entry_price)/entry_price
                intraday_call_close.append(profit_percentage)
                trade_status = 4
                print("IntraDay Timeout - Call Entry Closed")
                
                
            if buy == 0 and sell == 1 and trade == 1 and df.iloc[i]["dt"].time() == datetime.time(15,0,0):
                buy = 1
                trade = 0
                profit_percentage = (entry_price - df.iloc[i]['close'])/entry_price
                intraday_put_close.append(profit_percentage)
                trade_status = 14
                print("IntraDay Timeout - Put Entry Closed")
        
        if (df.iloc[i]["high"] > high):
            high = df.iloc[i]["high"]          # Day high
            #print('resistance_temp_high = ', high)
        if (df.iloc[i]["low"] < low):
            low = df.iloc[i]["low"]            # Day low
            #print('resistance_temp_low = ', low)
        
        if (df.iloc[i]["dt"].time() == datetime.time(15,15,0)):
            close = df.iloc[i]["close"]
            print("Close Price recorded = ", close)
            
            result.append([current_date, close, resistance, support, entry_price, stoploss, target_price, trade_status_encoding[trade_status]])

            p = (high + low + close)/3
            next_day_resistance = (p*2) - low
            next_day_support = (p*2) - high
            
            high = 0
            low = 99999
            buy = 0
            sell = 0
            trade_status = -1
            print("Current Date :- ", current_date)
            try:
                current_date = df.iloc[i+1]["dt"].date()
            except:
                pass
            daysCount += 1
            print('Day\'s Count = ', daysCount)
            print("\n")
            
            if resistance == -1:
                #print("One Time Registration")
                resistance = next_day_resistance
                support = next_day_support
        
print("Count of Call Target Hits = ", call_target_hit)
result_summary.append(["Count of Call Target Hits = ", call_target_hit])
try:
    avg = sum(intraday_call_close)/len(intraday_call_close)*100
except: 
    avg = 'Failed'
    pass
print("Count of Call closed for Intraday = ", len(intraday_call_close), "Avg % = ", avg)
result_summary.append(["Count of Call closed for Intraday = ", len(intraday_call_close), "Avg % = ", avg])
print("Count of Call StopLoss Hits = ", call_sl_hit)
result_summary.append(["Count of Call StopLoss Hits = ", call_sl_hit])
print("Count of Put Target Hits = ", put_target_hit)
result_summary.append(["Count of Put Target Hits = ", put_target_hit])
try:
    avg = sum(intraday_put_close)/len(intraday_put_close)*100 
except: 
    avg = 'Failed'
    pass
print("Count of Put closed for Intraday = ", len(intraday_put_close), "Avg % = ", avg)
result_summary.append(["Count of Put closed for Intraday = ", len(intraday_put_close), "Avg % = ", avg])
print("Count of Put StopLoss Hits = ", put_sl_hit)
result_summary.append(["Count of Put StopLoss Hits = ", put_sl_hit])

with open('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Indicator_PivotPointStandard_NIFTY50_BackTesting\\Results.csv', 'w') as OutputFile:
    # using csv.writer method from CSV package
    write = csv.writer(OutputFile)      
    write.writerow(result[0])
    write.writerows(result[1:])
    write.writerows(result_summary)    

print("\nReport Generated Successfully!!!")