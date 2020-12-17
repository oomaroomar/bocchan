import os
# Delete after done testing
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from requests import get

load_dotenv()
VANTAGE_TOKEN = os.getenv('ALPHA_VANTAGE_TOKEN')

market_api = 'https://www.alphavantage.co/query?'


def get_market_info_from_api(symbol: str, timeframe: str):
    if datetime.today().weekday() >= 5:
        return 'You\'re checking stock prices on the weekend, dumbfuck.'

    func = get_func(timeframe)
    interval = get_interval(func)

    stock_data = pd.read_csv(
        f'{market_api}function={func}&symbol={symbol}{interval}&apikey={VANTAGE_TOKEN}&datatype=csv')
    print(stock_data)
    stock_data = stock_data.iloc[::-1]
    print(stock_data)
    plt.plot(stock_data['timestamp'], stock_data['close'])
    # Reversing data frame doesn't reverse indices. This is a temporary (permanent) solution.
    plt.xticks([0, 24, 49, 74, 99], [stock_data['timestamp'][99][-8:-3], stock_data['timestamp'][74][-8:-3], stock_data['timestamp'][49][-8:-3],
                                     stock_data['timestamp'][24][-8:-3], stock_data['timestamp'][0][-8:-3]])
    plt.show()


def get_interval(func: str) -> str:
    if func == 'TIME_SERIES_INTRADAY':
        return '&interval=5min'
    return ''


def get_func(timeframe: str) -> str:
    if timeframe == 'day':
        return 'TIME_SERIES_INTRADAY'
    elif timeframe == 'week' or timeframe == 'month' or timeframe == 'biannual':
        return 'TIME_SERIES_DAILY'
    elif timeframe == 'max':
        return 'TIME_SERIES_WEEKLY'
    return 'TIME_SERIES_INTRADAY'


get_market_info_from_api('AAPL', 'day')
