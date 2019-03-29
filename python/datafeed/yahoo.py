#!/usr/bin/env python3
import pandas as pd
import fix_yahoo_finance as yf
from pandas_datareader import data as pdr


def get_close(stocks, start, end):
    yf.pdr_override() 
    start = pd.to_datetime(start) 
    end = pd.to_datetime(end)
    data = pdr.get_data_yahoo(stocks, start=start, end=end)['Adj Close']
    return data
