import pandas as pd
import numpy as np
import requests
import datetime
import pytz
import time
import json
import os

## Func: load_json
##  Args {name of security (str), start time (epoch datetime)}
##  Desc: requests JSON data of a security within 3 days of start time with 1 minute granularity
##  Returns: dataframe
def load_json(name, start_time):
    prefix = 'https://query1.finance.yahoo.com/v8/finance/chart/'
    
    URL = '{symbol}?symbol={symbol}&period1={end}&period2={begin}'.format(symbol=name, end=int(start_time - (3*24*60*60)), begin=int(start_time + (24*60*60)))
    suffix = '&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=QX.dgsOBXW9&corsDomain=finance.yahoo.com'

    res = requests.get(
        url=prefix + URL + suffix
    )
    return json.loads(res.content)

## Func: get_historical
##  Args {name of security (str), start time (datetime), length in minutes (int)}
##  Desc: Gets historical data for stock from start time - length in minutes to start time
##  Returns: 1D array of values separated by 1 min index
def get_historical(name, start_time, len_min):
    len_e = len_min * 60
    start_time = pytz.utc.localize(start_time)
    start_time = start_time.timestamp() - 60*60

    data = load_json(name, start_time)

    offset = data['chart']['result'][0]['meta']['gmtoffset']
    timestamps = offset + np.asarray(data['chart']['result'][0]['timestamp'])
    values = data['chart']['result'][0]['indicators']['quote'][0]['open']

    result = []
    for i in range(0, len(timestamps) - 1):
        timestamp = timestamps[i]
        if timestamp <= start_time and timestamp >= start_time - len_e:
            result.append(values[i])

    return result, data['chart']['result'][0]['meta']['regularMarketPrice']
