import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os
import sqlite3
from urllib.request import Request, urlopen
import json
import requests
import databento as db

dbdir = r'C:\Users\Sad_Matt\Desktop\Python\stocks\New folder'
os.chdir(dbdir)
conn = sqlite3.connect('stonks.db')
c = conn.cursor()
fields = 'TICKER ZCOUNT ZSCORE STD MEAN SMSCORE MVAL MSCORE EARNINGS RISING'
fields = fields.split(' ')

date_text = '%m-%d-%Y'
date_text = '%Y-%m-%d'


# Set the ticker for GME
ticker = "CPA"

i_p = 8
#    i_ps =  0   1   2   3    4    5    6    7   8   9   10   11   12
intervals = '1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo'
periods = [6, 59, 59, 59, 59, 59, 59, 59, 1000, 1000, 1000, 1000, 1000]
# i_ps =   0  1   2   3   4   5   6   7   8     9     10    11    12
intervals = intervals.split(', ')


def graphit(ticker):
    print(ticker)
    dX = []
    ticka = yf.Ticker(ticker)
    ticka = ticka.earnings_history
    for i in range(0, len(ticka)):
        dX.append(ticka.iloc[i].name.to_pydatetime())
    interval = intervals[i_p]
    end_date = datetime.datetime.now()
    data = yf.download(ticker, interval=interval, start=dX[0], end=end_date)
    D = []
    X = []
    Y = []
    for i in range(0, len(data['Close'])):
        datum = data['Close'].iloc[i]
        X.append(i)
        D.append(datum.name.to_pydatetime())
        Y.append(datum[ticker])
    Y = np.array(Y)
    mean = np.mean(Y)
    std = np.std(Y)
    mid_val = ((max(Y) - min(Y)) / 2) + min(Y)
    zD = [D[0]]
    zY = [data['Close'].iloc[0][ticker]]
    zcheck = True
    rising = False
    while zcheck:
        for i in range(1, len(data['Close'])):
            datum = data['Close'].iloc[i]
            zy = datum[ticker]
            if zy > mean + std:
                rising = True
                zcheck = False
            if zy < mean + std:
                rising = False
                zcheck = False
    zcount = 0
    print(f'std: {std}')
    print(mean + std)
    print(mean)
    print(mean - std)
    smscore = round(100 * std / mean, 2)
    print(f'std mean ration: {smscore}')
    for i in range(1, len(data['Close'])):
        datum = data['Close'].iloc[i]
        zy = datum[ticker]
        if rising:
            if zy > mean + std:
                zD.append(D[i])
                zY.append(Y[i])
                zcount = zcount + 1
                rising = False
        else:
            if zy < mean - std:
                zD.append(D[i])
                zY.append(Y[i])
                zcount = zcount + 1
                rising = True
    print("- - - - - - - - - - - - - - - - - - -")
    print(f'zcount: {zcount}')
    print(f'earnings: {len(ticka)}')
    zscore = round(100 * zcount / len(ticka), 2)
    print(f'zscore: {zscore}')
    print("- - - - - - - - - - - - - - - - - - -")
    earnings = len(ticka)
    mscore = round(100 * (mean - mid_val) / mean, 2)
    rscore = 'False'
    if rising:
        rscore = 'True'
    print("_____________________________________")
    query = 'INSERT INTO scores ('
    for field in fields:
        query = f'{query}{field}, '
    query = f'{query[:-2]}) VALUES ('
    vals = [ticker,
            zcount,
            zscore,
            round(std, 2),
            round(mean, 2),
            smscore,
            round(mid_val, 2),
            mscore,
            earnings,
            rscore]
    for val in vals:
        query = f'{query}?, '
    query = f'{query[:-2]})'
    c.execute(query, list(vals))
    conn.commit()

#graphit('CPA')


def get_tickers():
    client = db.Historical()
    data = client.timeseries.get_range(
        dataset='XNAS.ITCH',
        schema='definition',
        symbols='ALL_SYMBOLS',
        start='2023-08-03',
        end='2023-08-03'
    )
    df = data.to_df()
    print(df['raw_symbol'])


def get_all_companies(headers):
    companyTickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=headers)
    company_dct = companyTickers.json()
    cik_lst = [str(company_dct[x]['cik_str']).zfill(10) for x in company_dct]

    return cik_lst

headers = {'User-Agent': "matt.tigrett@gmail.com"}
cik_lst = get_all_companies(headers)
print(len(cik_lst))

