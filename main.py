import pandas as pd
import numpy as np
import multiprocessing as mp
from datetime import datetime
import random
import math
import time
import os
from data_requests import get_historical
import plotly.express as px

## Func: write_to_csv
##  Args {arr (array)}
##  Desc: Writes array to CSV
def write_to_csv(arr):
    csv = open('./output/output.csv', 'a+')
    for v in arr:
        csv.write('%.14f' % v)
        csv.write('\n')
    csv.close()

## Func: get_volatility
##  Args {prices (array), spot_price (number)}
##  Desc: Calculates volatility from previous financial data
##  Returns: volatility (number)
def get_volatility(prices, spot_price):
    t_steps = len(prices) + 1
    prices = np.append(prices, spot_price)
    mean_price = np.nanmean(prices)
    std_dev = np.nanstd(prices)

    return std_dev / 100, t_steps

## Func: rand
##  Args {mean (number), std_dev (number)}
##  Desc: Given mean and std_dev, gets normally distributed random number
##  Returns: normally distributed random number (number)
def rand(mean, std_dev):
    return np.random.normal(mean, std_dev)

## Func: find_mean
##  Args {arr (array), num_loops (num loops)}
##  Desc: Returns mean value of array
##  Returns: np array
def find_mean(arr, num_loops):
    return np.sum(np.asarray(arr) / num_loops, axis=0)    

## Func: black_scholes
##  Args {spot_price (number), t_steps (number), risk_rate (number), volatility (number)}
##  Desc: Simulates black-scholes model
##  Returns: array
def black_scholes(spot_price, t_steps, risk_rate, volatility):
    delta_t = 1 / t_steps
    prices = np.zeros(t_steps)
    prices[0] = spot_price
    norm_rand = np.zeros(t_steps)

    for i in range(t_steps):
        norm_rand[i] = rand(0, 1)
        if i + 1 < t_steps:
            prices[i + 1] = prices[i] * math.exp(((risk_rate - (math.pow(volatility, 2) / 2)) * delta_t) + (volatility * norm_rand[i] * math.sqrt(delta_t)))

    return prices

## Func: run_inner
##  Args {i (number), in_monte (number), t_steps (number), spot_price (number), risk_rate (number), volatility (number)}
##  Desc: Used for parellised monte-carlo simulation in [model()]
##  Returns: np array
def run_inner(i, in_monte, t_steps, spot_price, risk_rate, volatility):
    stock = np.zeros((in_monte, t_steps))
    for j in range(0, in_monte):
        stock[j] = black_scholes(spot_price, t_steps, risk_rate, volatility)
    
    return find_mean(stock, in_monte)

## Func: model
##  Args: (security (str), start_time (datetime), len_t (number), risk_rate (number))
##  Desc: Forecasts security prices using prev. (start_time - len_t) data
def model(security, start_time, len_t, risk_rate):
    print("Forecast started ->", datetime.now().strftime("%H:%M:%S"))

    in_monte, out_monte = 100, 10000
    data, spot_price = get_historical(security, start_time, len_t)
    data = np.array(data, dtype=np.float)
    data = data[~np.isnan(data)]

    volatility, t_steps = get_volatility(data, spot_price)
    avg_stock = np.zeros((out_monte, t_steps))

    pool = mp.Pool()
    iterable = list(np.zeros((out_monte, 5)))
    for i in range(0, out_monte):
        iterable[i] = [i, in_monte, t_steps, spot_price, risk_rate, volatility]
    avg_stock = pool.starmap(run_inner, iterable)

    opt_stock = find_mean(avg_stock, out_monte)

    write_to_csv(opt_stock)
    
    print("Forecast produced ->", datetime.now().strftime("%H:%M:%S"))


if __name__ == "__main__":
    model(
        'AMZN',                                # Stock name
        datetime(2020, 4, 13, 13, 00, 00),     # Retrospective start time
        180,                                   # Length of analytical date (mins)
        0.001                                  # Risk free interest rate
    )
