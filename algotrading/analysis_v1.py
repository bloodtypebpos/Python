import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os

dbdir = r'C:\Users\Sad_Matt\Desktop\Python\stocks\New folder'
os.chdir(dbdir)

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


def graphit(ticker, earning_time, showit):
    dX = []
    ticka = yf.Ticker(ticker)
    # print(ticka.earnings_dates.iloc[6])
    # print(" - - - - - - - - - - - - - - - -")
    # print(ticka.earnings_dates.iloc[6].name)
    print(ticka.earnings_history)
    # original below
    # ticka = ticka.earnings_dates
    # for i in range(0, len(ticka)):
    #    dX.append(ticka.iloc[i].name.to_pydatetime())
    ticka = ticka.earnings_history
    for i in range(0, len(ticka)):
        dX.append(ticka.iloc[i].name.to_pydatetime())

    # Define the interval and dates for 59 days back
    interval = intervals[i_p]
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=periods[i_p])  # 59 days back from today

    # Download 5-minute interval data between the specified start and end dates
    #data = yf.download(ticker, interval=interval, start=dX[len(dX)-1], end=end_date) # original
    data = yf.download(ticker, interval=interval, start=dX[0], end=end_date)

    D = []
    X = []
    Y = []

    for i in range(0, len(data['Close'])):
        datum = data['Close'].iloc[i]
        X.append(i)
        D.append(datum.name.to_pydatetime())
        Y.append(datum[ticker])

    fig, ax = plt.subplots(figsize=(20, 12))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_text))

    Y = np.array(Y)
    mean = np.mean(Y)
    std = np.std(Y)
    mid_val = ((max(Y) - min(Y)) / 2) + min(Y)
    M = []
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
    print(mean + std)
    print(mean)
    print(mean - std)
    for i in range(1, len(data['Close'])):
        datum = data['Close'].iloc[i]
        zy = datum[ticker]
        if rising:
            if zy > mean + std:
                print(zy)
                zD.append(D[i])
                zY.append(Y[i])
                zcount = zcount + 1
                rising = False
        else:
            if zy < mean - std:
                print(zy)
                zD.append(D[i])
                zY.append(Y[i])
                zcount = zcount + 1
                rising = True

    for i in range(0, len(Y)):
        M.append(mid_val)
    M = np.array(M)
    ax.fill_between(D, M, Y, where=(M < Y), color='green', alpha=0.5)
    ax.fill_between(D, M, Y, where=(M > Y), color='red', alpha=0.5)
    ax.plot([D[0], end_date], [mid_val, mid_val], color='black')
    ax.plot([D[0], end_date], [mean, mean], color='purple', linewidth=4)
    ax.plot([D[0], end_date], [mean + std, mean + std], color='blue', linewidth=4)
    ax.plot([D[0], end_date], [mean - std, mean - std], color='red', linewidth=4)
    for dx in dX:
        ddx = dx.strftime(date_text)
        ddx = datetime.datetime.strptime(ddx, date_text)
        if ddx < end_date:
            ax.plot([dx, dx], [min(Y), max(Y)], color='Red')
    ax.plot(D, Y)
    ax.plot(zD, zY, color='cyan')
    print(f'zcount: {zcount}')
    fontsize = 30
    ax.set_title(f'{ticker}-{earning_time}', fontsize=fontsize)
    plt.xlabel('Date', fontsize=fontsize)
    plt.ylabel('Price', fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    plt.xticks(rotation=45)
    plt.savefig(f'{ticker}-{earning_time}.png', bbox_inches='tight')
    if showit:
        plt.show()


def batch():
    morning = 'BIDU PDD DE BJ VSTS WMG BEKE IQ NNOX SCVL'
    evening = 'INTU ESTC GAP ROST NTAP CPRT UGI MATW NGVC'
    morning = morning.split(' ')
    evening = evening.split(' ')
    tickerz = [morning, evening]

    for i in range(0, 2):
        tickers = tickerz[i]
        earning_time = 'Before Open'
        if i > 0:
            earning_time = 'After Close'
        for ticker in tickers:
            try:
                print(ticker)
                graphit(ticker, earning_time, False)
            except:
                print(f'There was an issue with: {ticker}')
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")


graphit('CPA', 'NA', True)


