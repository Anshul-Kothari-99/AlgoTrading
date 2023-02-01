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
Data Extraction failed for - 179 Companies

temp1 = ['3IINFOTECH.NS', 'ABMINTLTD.NS', 'ADANIGAS.NS', 'ADHUNIK.NS', 'ADHUNIKIND.NS', 'ADLABS.NS', 'AGCNET.NS', 'AHLWEST.NS', 'AIONJSW.NS', 
         'ALBK.NS', 'ALCHEM.NS', 'ALOKTEXT.NS', 'ANDHRABANK.NS', 'ANSALHSG.NS', 'ARCOTECH.NS', 'ARIHANT.NS', 'ARROWTEX.NS', 'ATLASCYCLE.NS', 
         'AUTOLITIND.NS', 'BARTRONICS.NS', 'BILENERGY.NS', 'BLUEBLENDS.NS', 'BOROSIL.NS', 'BSELINFRA.NS', 'CADILAHC.NS', 'CANDC.NS', 
         'CASTEXTECH.NS', 'CEBBCO.NS', 'CELESTIAL.NS', 'CESCVENT.NS', 'CHROMATIC.NS', 'CIMMCO.NS', 'CKFSL.NS', 'CNOVAPETRO.NS', 
         'CORPBANK.NS', 'COSMOFILMS.NS', 'COX&KINGS.NS', 'CURATECH.NS', 'DEEPIND.NS', 'DHFL.NS', 'DIAPOWER.NS', 'DIGJAMLTD.NS', 'DOLAT.NS', 
         'DQE.NS', 'EASUNREYRL.NS', 'EDL.NS', 'EMCO.NS', 'EON.NS', 'ESSELPACK.NS', 'EUROCERA.NS', 'EUROMULTI.NS', 'FAIRCHEM.NS', 
         'GALLISPAT.NS', 'GAMMNINFRA.NS', 'GARDENSILK.NS', 'GDL.NS', 'GLOBOFFS.NS', 'GSKCONS.NS', 'GTNIND.NS', 'GTNTEX.NS', 'HARITASEAT.NS', 
         'HEXAWARE.NS', 'HINDSYNTEX.NS', 'HOTELEELA.NS', 'HOTELRUGBY.NS', 'HSIL.NS', 'IBULISL.NS', 'IBVENTURES.NS', 'INDOSOLAR.NS', 
         'INFRATEL.NS', 'INTEGRA.NS', 'IPAPPM.NS', 'IVRCLINFRA.NS', 'JAIHINDPRO.NS', 'JAINSTUDIO.NS', 'JINDCOT.NS', 'JIYAECO.NS', 
         'JMTAUTOLTD.NS', 'JUBILANT.NS', 'JUMPNET.NS', 'JVLAGRO.NS', 'KALYANI.NS', 'KARDA.NS', 'KESARENT.NS', 'KGL.NS', 'KSERASERA.NS', 
         'KSK.NS', 'KTIL.NS', 'KWALITY.NS', 'LAKSHVILAS.NS', 'LINCPEN.NS', 'LTI.NS', 'MAGMA.NS', 'MAJESCO.NS', 'MANGTIMBER.NS', 'MANPASAND.NS', 
         'MAXINDIA.NS', 'MCDHOLDING.NS', 'MEGH.NS', 'METKORE.NS', 'MIC.NS', 'MINDAIND.NS', 'MINDTREE.NS', 'MOTHERSUMI.NS', 'MUKANDENGG.NS', 
         'MVL.NS', 'NAGAROIL.NS', 'NBVENTURES.NS', 'NIITTECH.NS', 'NIRAJISPAT.NS', 'NITINFIRE.NS', 'NTL.NS', 'OISL.NS', 'OMMETALS.NS', 
         'OPTOCIRCUI.NS', 'ORIENTBANK.NS', 'ORIENTREF.NS', 'ORTINLABSS.NS', 'PAEL.NS', 'PAPERPROD.NS', 'PARABDRUGS.NS', 'PATSPINLTD.NS', 
         'PDSMFL.NS', 'PETRONENGG.NS', 'PHILIPCARB.NS', 'PIRPHYTO.NS', 'PRABHAT.NS', 'PRADIP.NS', 'PROSEED.NS', 'PROVOGE.NS', 'PSL.NS', 
         'PUNJLLOYD.NS', 'RAJRAYON.NS', 'RAMSARUP.NS', 'RNAM.NS', 'ROHITFERRO.NS', 'RTNINFRA.NS', 'RUCHISOYA.NS', 'SANGHVIFOR.NS', 
         'SELMCL.NS', 'SEZAL.NS', 'SHIRPUR-G.NS', 'SHRIRAMCIT.NS', 'SHRIRAMEPC.NS', 'SICAGEN.NS', 'SMPL.NS', 'SORILINFRA.NS', 'SRIPIPES.NS', 
         'STINDIA.NS', 'STRTECH.NS', 'SUBEX.NS', 'SUJANAUNI.NS', 'SUPPETRO.NS', 'SYNCOM.NS', 'SYNDIBANK.NS', 'TALWALKARS.NS', 'TALWGYM.NS', 
         'TATAGLOBAL.NS', 'TATASTLBSL.NS', 'TCIDEVELOP.NS', 'TECHNOFAB.NS', 'THIRUSUGAR.NS', 'TMRVL.NS', 'UNIPLY.NS', 'UNITEDBNK.NS', 
         'UNITY.NS', 'UTTAMSTL.NS', 'UVSL.NS', 'VIDEOIND.NS', 'VIKASMCORP.NS', 'VIMALOIL.NS', 'WABCOINDIA.NS', 'WEIZFOREX.NS', 'WINSOME.NS', 
         'XLENERGY.NS', 'ZENITHBIR.NS', 'ZICOM.NS', 'ZODJRDMKJ.NS', 'ZUARIGLOB.NS']
'''

for ticker in tickers[:]:
    stock_data = yf.download(ticker[0], start = start_date, end = end_date, interval = timeframe)
    #print('Ticker Name -------------> ', ticker[0])
    if stock_data.shape[0] > 0:
        stock_data = stock_data.reset_index()
        stock_data['Date'] = pd.to_datetime(stock_data['Datetime']).dt.date
        stock_data['Time'] = pd.to_datetime(stock_data['Datetime']).dt.time
        stock_data.drop(['Datetime', 'Adj Close'], axis=1, inplace=True)
        stock_data.to_csv('D:\\NSE_Stocks_5m_hist_data\\' + ticker[0] + ".csv", index=False)
        #print(stock_data.head())
        #print('\n')

    else:
        print('Data Download Failed for -------------> ', ticker[0], '\n')
        failed_for.append(ticker[0])
        
print('************************* Finished *************************\n')
print(failed_for)
print('Data Extraction failed for - ',len(failed_for), ' Companies')