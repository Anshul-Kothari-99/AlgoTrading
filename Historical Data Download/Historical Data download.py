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

failed_for = []

'''
temp = ['3IINFOTECH.NS', 'ADANIGAS.NS', 'ADHUNIKIND.NS', 'ADLABS.NS', 'AGCNET.NS', 'AGLSL.NS', 'AHLWEST.NS', 'AIONJSW.NS', 
        'ALBK.NS', 'ANDHRABANK.NS', 'ANSALHSG.NS', 'ARIHANT.NS', 'ARROWTEX.NS', 'BARTRONICS.NS', 'BHARATFIN.NS', 
        'BLUEBLENDS.NS', 'BOROSIL.NS', 'BSELINFRA.NS', 'CADILAHC.NS', 'CEBBCO.NS', 'CELESTIAL.NS', 'CESCVENT.NS', 
        'CHROMATIC.NS', 'CIMMCO.NS', 'CNOVAPETRO.NS', 'CORPBANK.NS', 'COSMOFILMS.NS', 'COX&KINGS.NS', 'DEEPIND.NS', 
        'DHFL.NS', 'DOLPHINOFF.NS', 'DQE.NS', 'EASUNREYRL.NS', 'EON.NS', 'ESSELPACK.NS', 'EXCELCROP.NS', 'FAIRCHEM.NS', 
        'GALLISPAT.NS', 'GAMMNINFRA.NS', 'GARDENSILK.NS', 'GDL.NS', 'GLOBOFFS.NS', 'GRUH.NS', 'GSKCONS.NS', 'GTNIND.NS', 
        'GUJFLUORO.NS', 'HARITASEAT.NS', 'HEXAWARE.NS', 'HIGHGROUND.NS', 'HINDSYNTEX.NS', 'HINDUJAVEN.NS', 'HOTELEELA.NS', 
        'HSIL.NS', 'IBVENTURES.NS', 'INDIA VIX.NS', 'INFRATEL.NS', 'IPAPPM.NS', 'JMTAUTOLTD.NS', 'JUBILANT.NS', 'KARDA.NS', 
        'KESARENT.NS', 'KSERASERA.NS', 'KSK.NS', 'KTIL.NS', 'KWALITY.NS', 'LAKSHVILAS.NS', 'LTI.NS', 'MAGMA.NS', 'MAJESCO.NS', 
        'MANPASAND.NS', 'MAXINDIA.NS', 'MCDHOLDING.NS', 'MEGH.NS', 'MINDAIND.NS', 'MINDTREE.NS', 'MONSANTO.NS', 'MOTHERSUMI.NS', 
        'MUKANDENGG.NS', 'NAGAROIL.NS', 'NBVENTURES.NS', 'NIITTECH.NS', 'NITESHEST.NS', 'NITINFIRE.NS', 'OMMETALS.NS', 
        'OPTOCIRCUI.NS', 'ORIENTBANK.NS', 'ORIENTREF.NS', 'ORTINLABSS.NS', 'PAEL.NS', 'PAPERPROD.NS', 'PATSPINLTD.NS', 
        'PDSMFL.NS', 'PHILIPCARB.NS', 'PRABHAT.NS', 'PRAKASHCON.NS', 'PROSEED.NS', 'PSL.NS', 'python_file_read.NS', 
        'RNAM.NS', 'RTNINFRA.NS', 'SELMCL.NS', 'SHRIRAMCIT.NS', 'SHRIRAMEPC.NS', 'SICAGEN.NS', 'SORILINFRA.NS', 'SRIPIPES.NS', 
        'STRTECH.NS', 'SUBEX.NS', 'SUPPETRO.NS', 'SYNDIBANK.NS', 'TALWALKARS.NS', 'TALWGYM.NS', 'TATAGLOBAL.NS', 
        'TATASPONGE.NS', 'TATASTLBSL.NS', 'TCIDEVELOP.NS', 'TECHNOFAB.NS', 'TMRVL.NS', 'UNIPLY.NS', 'UNITEDBNK.NS', 
        'UTTAMSTL.NS', 'UVSL.NS', 'VIKASMCORP.NS', 'WABCOINDIA.NS', 'WEIZFOREX.NS', 'ZODJRDMKJ.NS', 'ZUARIGLOB.NS']

127 total elements
'''

for ticker in tickers[:]:
    stock_data = yf.download(ticker[0], start = start_date, end = end_date, interval = timeframe)
    #print('Ticker Name -------------> ', ticker[0])
    #print(stock_data.shape[0])
    if stock_data.shape[0] > 0:
        stock_data = stock_data.reset_index()
        stock_data['Date'] = pd.to_datetime(stock_data['Datetime']).dt.date
        stock_data['Time'] = pd.to_datetime(stock_data['Datetime']).dt.time
        stock_data.drop(['Datetime', 'Adj Close'], axis=1, inplace=True)
        stock_data.to_csv('D:\\NSE_Stocks_5m_hist_data\\' + ticker[0] + ".csv", index=False)
        #print(stock_data.head())
        #print('\n')
        #print(stock_data.columns)
    else:
        print('Data Download Failed for -------------> ', ticker[0], '\n')
        failed_for.append(ticker[0])
        
print('************************* Finished *************************\n')
print(failed_for)
print('Data Extraction failed for - ',len(failed_for), ' Companies')