# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 00:28:22 2023

@author: Anshul Kothari
kotharianshul.1998@gmail.com
"""
import pandas as pd
from os import walk
import datetime
init_time = datetime.datetime.now()

mypath = "D:\\NSE_Stocks_5m_hist_data\\pre processed data files\\"
# "D:\\Python Scripts\\shares Analysis\\preprocessed_5_min_equity_data\\"
files_list = next(walk(mypath), (None, None, []))[2]  # This would extract all the files(shares) names present in the folder

result_summary_for_NSE_stocks = []
failed_for = []
count = 0

# HyperParameters - to be tunned
target_percentage_of_profit_for_call = 1    # 1.8, 1.845, 2.4, 4.2, 6.7
target_percentage_of_sl_for_call = 0.31     # try keeping stoploss below the confirmation factor
call_confirmation = 1.003
call_red_candle_length_check = 1.5
# call_green_candle_length_check = 0.77       # 1
call_third_candle_length_check = 1.2

target_percentage_of_profit_for_put = 1   # 0.83 with 0.9998 confirmation factor #0.89
target_percentage_of_sl_for_put = 0.31  # 0.535, 0.54, 495
put_confirmation = 0.997      # 0.9998
put_green_candle_length_check = 1.5
# put_red_candle_length_check = 0.77       # 1
put_third_candle_length_check = 1.2

timeframe = 5    # Enter Timeframe in minutes(5m/15m/30m only) - enter timeframe less than 30mins

for stock in files_list:
    # stock = 'NIFTY50_5min.csv'
    testcases_file_path = mypath + stock
    count += 1

    try:
        df = pd.read_csv(testcases_file_path)
        df.dt = pd.to_datetime(df.dt)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        # df = df[4028:4105]  # To limit the data / Number of days - 1600 = Approx 31 days
        # print(df)

        result_summary = []
        daysCount = 0

        resistance = 999999
        support = 0
        entry_price = 0
        target_price = 0
        stoploss = 0

        count_no_trades = 0
        current_date = df.iloc[0]["dt"].date()
        date_exception = []
        start_date = current_date
        no_trades_dates = []

        high = 0
        low = 99999
        buy = 0
        sell = 0
        trade = 0
        trade_status = -1

        intraday_call_close = []
        intraday_put_close = []
        call_target_hit = 0
        call_sl_hit = 0
        put_target_hit = 0
        put_sl_hit = 0

        call_target_hit_dates = []
        call_sl_hit_dates = []
        call_closed_dates = []
        put_target_hit_dates = []
        put_sl_hit_dates = []
        put_closed_dates = []

        bull_harami_candle_number = -1
        bull_harami = -1
        bull_harami_count = 0
        bull_harami_instance = []
        bear_harami_candle_number = -1
        bear_harami = -1
        bear_harami_count = 0
        bear_harami_instance = []

        trade_status_encoding = {-1: 'No Trade Taken',
                                 1: 'Call - Buy',
                                 2: 'Call Target Hit',
                                 3: 'Call StopLoss Hit',
                                 4: 'IntraDay Timeout - Call Entry Closed',
                                 11: 'Put - Buy',
                                 12: 'Put Target Hit',
                                 13: 'Put StopLoss Hit',
                                 14: 'IntraDay Timeout - Put Entry Closed'}

        # print("Starting Date ----------> ", start_date)

        for i in range(len(df)):

            if df.iloc[i]["dt"].date() == current_date:

                debug_candle = str(df.iloc[i]["dt"])

                # Bull Harami Formation (Big Red followed by inside Green)
                if ((i+3) < len(df)
                    and df.iloc[i]['open'] > df.iloc[i]['close']     # check for 1st red candle
                    and df.iloc[i+1]['open'] < df.iloc[i+1]['close']     # check 2nd for green candle
                    and df.iloc[i]['open'] > df.iloc[i+1]['high']
                    and df.iloc[i]['close'] < df.iloc[i+1]['low']):
                    bull_harami_count += 1
                    bull_harami_instance.append(str(df.iloc[i]['dt']))

                    call_red_candle_length = (df.iloc[i]['open'] - df.iloc[i]['close']) / df.iloc[i]['close'] * 100
                    if (bull_harami == -1 
                        and df.iloc[i]['high'] < df.iloc[i+2]['close']  # check 3rd candle closes above 1st candle high
                        and call_red_candle_length >= call_red_candle_length_check   # check 1st/Red candle length
                        and df.iloc[i+2]['open'] < df.iloc[i+2]['close']   # check - 3rd candle is green
                        and ((df.iloc[i+2]['close'] - df.iloc[i+2]['open']) / df.iloc[i+2]['open'] * 100) >= call_third_candle_length_check    # check 3rd/green candle length 
                        and ((df.iloc[i+1]['close'] - df.iloc[i+1]['open']) / df.iloc[i+1]['open'] * 100) >= (call_red_candle_length/2)    # check 2nd/green candle length 
                        and df.iloc[i+2]["dt"].time() < datetime.time(14, 20, 0)
                        and trade == 0 and buy != 1 and sell != 1):
                        # Write Confirmation Logic here
                        resistance = df.iloc[i+2]['close'] * call_confirmation
                        bull_harami_candle_number = i
                        bull_harami = 1

                if (bull_harami == 1
                    and i > bull_harami_candle_number + 2
                    and df.iloc[i]["dt"].time() < datetime.time(14, 35, 0)
                    and df.iloc[i]['high'] > resistance):
                    trade = 1
                    buy = 1
                    entry_price = resistance
                    target_price = entry_price * ((100 + target_percentage_of_profit_for_call)/100)
                    stoploss = entry_price * ((100 - target_percentage_of_sl_for_call)/100)
                    trade_status = 1
                    resistance = 999999
                    # print("Call - Buy")

                # Bear Harami Formation (Big Green followed by inside Red)
                if ((i+3) < len(df)
                    and df.iloc[i]['open'] < df.iloc[i]['close']     # check for 1st green candle
                    and df.iloc[i+1]['open'] > df.iloc[i+1]['close']     # check for 2nd red candle
                    and df.iloc[i]['open'] < df.iloc[i+1]['low']
                    and df.iloc[i]['close'] > df.iloc[i+1]['high']):
                    bear_harami_count += 1
                    bear_harami_instance.append([str(current_date), current_date.weekday()])

                    put_green_candle_length = (df.iloc[i]['close'] - df.iloc[i]['open']) / df.iloc[i]['open'] * 100
                    if (bear_harami == -1
                        and df.iloc[i]['low'] > df.iloc[i+2]['close']  # check 3rd candle closes below 1st candle low
                        and put_green_candle_length >= put_green_candle_length_check   # check 1st/green candle length
                        and df.iloc[i+2]['open'] > df.iloc[i+2]['close']   # check - 3rd candle is red
                        and ((df.iloc[i+2]['open'] - df.iloc[i+2]['close']) / df.iloc[i+2]['close'] * 100) >= put_third_candle_length_check    # check 3rd/red candle length 
                        and ((df.iloc[i+1]['open'] - df.iloc[i+1]['close']) / df.iloc[i+1]['close'] * 100) >= (put_green_candle_length/2)    # check 2nd/red candle length 
                        and df.iloc[i+2]["dt"].time() < datetime.time(14, 20, 0)
                        and trade == 0 and buy != 1 and sell != 1):
                        # Write Confirmation Logic here
                        support = df.iloc[i+2]['close'] * put_confirmation
                        bear_harami_candle_number = i
                        bear_harami = 1

                if (bear_harami == 1
                    and i > bear_harami_candle_number + 2
                    and df.iloc[i]["dt"].time() < datetime.time(14, 35, 0)
                    and df.iloc[i]['low'] < support):
                    trade = 1
                    sell = 1
                    entry_price = support
                    target_price = entry_price * ((100 - target_percentage_of_profit_for_put)/100)
                    stoploss = entry_price * ((100 + target_percentage_of_sl_for_put)/100)
                    trade_status = 11
                    support = 0
                    #print("Put - Buy")

                if (buy == 1 and sell == 0 and trade == 1 and bull_harami == 1
                    and i > bull_harami_candle_number + 2):
                    # Call Status Checks
                    if (df.iloc[i]['high'] > target_price):
                        sell = 1
                        trade = 0
                        call_target_hit = call_target_hit + 1
                        trade_status = 2
                        bull_harami = -1
                        call_target_hit_dates.append([str(current_date), current_date.weekday()])
                        # print("Call Target Hit")
                    elif (df.iloc[i]['low'] < stoploss                        # if changed to elif ------------- compare results
                        and i > bull_harami_candle_number + 3
                        ):
                        sell = 1
                        trade = 0
                        call_sl_hit = call_sl_hit + 1
                        trade_status = 3
                        bull_harami = -1
                        call_sl_hit_dates.append([str(current_date), current_date.weekday()])
                        # print("Call Stoploss Hit")

                if (buy == 0 and sell == 1 and trade == 1 and bear_harami == 1
                    and i > bear_harami_candle_number + 2):
                    # Put Status Check
                    if (df.iloc[i]['low'] < target_price):
                        buy = 1
                        trade = 0
                        put_target_hit = put_target_hit + 1
                        trade_status = 12
                        bear_harami = -1
                        put_target_hit_dates.append([str(current_date), current_date.weekday()])
                        #print("Put Target Hit")
                    elif (df.iloc[i]['high'] > stoploss
                        and i > bear_harami_candle_number + 3
                        ):
                        buy = 1
                        trade = 0
                        put_sl_hit = put_sl_hit + 1
                        trade_status = 13
                        bear_harami = -1
                        put_sl_hit_dates.append([str(current_date), current_date.weekday()])
                        #print("Put Stoploss Hit")
                
                if (buy == 1 and sell == 0 and trade == 1 and bull_harami == 1
                    and df.iloc[i]["dt"].time() >= datetime.time(15, 10, 0)):
                    sell = 1
                    trade = 0
                    profit_percentage = (df.iloc[i]['close'] - entry_price)/entry_price
                    intraday_call_close.append(profit_percentage)
                    trade_status = 4
                    bull_harami = -1
                    resistance = 999999
                    call_closed_dates.append([str(current_date), current_date.weekday()])
                    # print("IntraDay Timeout - Call Entry Closed")

                if (buy == 0 and sell == 1 and trade == 1 and bear_harami == 1
                    and df.iloc[i]["dt"].time() >= datetime.time(15, 10, 0)):
                    buy = 1
                    trade = 0
                    profit_percentage = (entry_price - df.iloc[i]['close'])/entry_price
                    intraday_put_close.append(profit_percentage)
                    trade_status = 14
                    bear_harami = -1
                    support = 0
                    put_closed_dates.append([str(current_date), current_date.weekday()])
                    #print("IntraDay Timeout - Put Entry Closed")

                '''
                # Recording Day High and Low
                if (df.iloc[i]["high"] > high):
                    high = df.iloc[i]["high"]          # Day high
                    #print('resistance_temp_high = ', high)
                if (df.iloc[i]["low"] < low):
                    low = df.iloc[i]["low"]            # Day low
                    #print('resistance_temp_low = ', low)
                '''

                if (df.iloc[i]["dt"].time() == datetime.time(15, (30-timeframe), 0)):
                    close = df.iloc[i]["close"]

                    if trade_status == -1:
                        count_no_trades += 1
                        no_trades_dates.append([str(current_date), current_date.weekday()])
                        # print(trade_status_encoding[trade_status])

                    high = 0
                    low = 99999
                    buy = 0
                    sell = 0
                    trade_status = -1
                    bull_harami = -1
                    bear_harami = -1
                    # print("Current Date :- ", current_date)
                    try:
                        current_date = df.iloc[i+1]["dt"].date()
                    except:
                        date_exception.append([str(current_date), current_date.weekday()])
                        pass
                    daysCount += 1
                    # print('Day\'s Count = ', daysCount)
                    # print("\n")
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

        # print('*********', count, ' - ' + stock + ' *********')
        '''
        print("Count of Call Target Hits = ", call_target_hit)
        result_summary.append(["Count of Call Target Hits = ", call_target_hit])
        '''
        try:
            avg_call = sum(intraday_call_close)/len(intraday_call_close)*100
        except: 
            avg_call = 0  # Failed
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
            avg_put = 0   # Failed
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
        print("\nDates on which Call Timed out", call_closed_dates)

        print("\nDates on which Put Targets got Hit", put_target_hit_dates)
        print("\nDates on which Put SL got Hit", put_sl_hit_dates)
        print("\nDates on which Put Timed out", put_closed_dates)

        print("\nDates on which NO Trades were taken", no_trades_dates)
        '''

        delta_days = call_target_hit + len(intraday_call_close) + call_sl_hit + put_target_hit + len(intraday_put_close) + put_sl_hit + len(no_trades_dates) - daysCount
        result_summary_for_NSE_stocks.append([stock[:-4],
                                              bull_harami_count,
                                              bull_harami_instance,
                                              bear_harami_count,
                                              bear_harami_instance,
                                              call_target_hit,
                                              len(intraday_call_close),
                                              avg_call,
                                              call_sl_hit,
                                              call_target_hit_dates,
                                              call_sl_hit_dates,
                                              call_closed_dates,
                                              put_target_hit,
                                              len(intraday_put_close),
                                              avg_put,
                                              put_sl_hit,
                                              put_target_hit_dates,
                                              put_sl_hit_dates,
                                              put_closed_dates,                                              
                                              count_no_trades,
                                              net_call,
                                              net_put,
                                              net_call + net_put,
                                              start_date,
                                              current_date,
                                              daysCount,
                                              # delta_days
                                              ])
        if (call_target_hit > 0) or (call_sl_hit > 0):
            print(count, '\t', stock[:-4], '\t\t', bull_harami_count, '\t\t', 'Call --> ', (call_target_hit, call_sl_hit))
        elif (put_target_hit > 0) or (put_sl_hit > 0):
            print(count, '\t', stock[:-4], '\t\t', bear_harami_count, '\t\t', 'Put --> ', (put_target_hit, put_sl_hit))
        else:
            print(count)
        bull_harami_count = 0
        bear_harami_count = 0

    except:
        # print(e)   Exception as e
        failed_for.append(stock[:-4])
        print('Analysis Failed for -------------> ', stock[:-4], i)
        pass

result_summary_for_NSE_stocks = pd.DataFrame(result_summary_for_NSE_stocks)
result_summary_for_NSE_stocks.columns = ["Stock Symbol",
                                         "Bull Harami Count",
                                         "Bull Harami Dates",
                                         "Bear Harami Count",
                                         "Bear Harami Dates",
                                         "Call Target Hits Count",
                                         "Call closed for Intraday Count",
                                         "Call Avg %",
                                         "Call StopLoss Hits Count",
                                         "Call Targets Hit Dates",
                                         "Call SL Hit Dates",
                                         "Call Closed Dates",
                                         "Put Target Hits Count",
                                         "Put closed for Intraday Count",
                                         "Put Avg %",
                                         "Put StopLoss Hits Count",
                                         "Put Targets Hit Dates",
                                         "Put SL Hit Dates",
                                         "Put Closed Dates",
                                         "No Trades Taken Count",
                                         "Net Call Returns",
                                         "Net Put Returns",
                                         "Net Returns",
                                         "Starting Date",
                                         "Last Date",
                                         "Number of days run",
                                         # "Delta Days"
                                         ]

print(result_summary_for_NSE_stocks)
result_summary_for_NSE_stocks.to_csv('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Indicator_Harami_BackTesting\\Stategy_Evaluation_on_Stocks.csv', index=False)

print('\nFailed for -------------> ', len(failed_for), failed_for)

'''
with open('C:\\Users\\kotha\\OneDrive\\Desktop\\Algo Trading Repo\\Indicator_PivotPointStandard_NIFTY50_BackTesting\\Results.csv', 'w') as OutputFile:
    # using csv.writer method from CSV package
    write = csv.writer(OutputFile)
    write.writerow(result[0])
    write.writerows(result[1:])
    write.writerows(result_summary)
'''
print("\n*********************************************************************")
print("Report Generated Successfully!!!")

fin_time = datetime.datetime.now()
print("Code Execution completed in ---->", (fin_time - init_time))