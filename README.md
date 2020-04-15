# Stockmarket forecasting: Black-Scholes and Monte Carlo simulations
### Python implementation of stockmarket forecasting using Black-Scholes model and parallelised Monte Carlo simulations


Run instructions:
 - Install requirements.txt
 - In main.py, modify following function call for desired variables:
 ```
    model(
        'AMZN',                                # Stock name
        datetime(2020, 4, 13, 13, 00, 00),     # Retrospective start time
        180,                                   # Length of analytical date (mins)
        0.001                                  # Risk free interest rate
    )
 ```
 - Run 'main.py'



To do list:
 - [X] Load 1 minute granularity security data from Y! Finance
 - [X] Implement Black-Scholes and Monte Carlo simulations for forecasting prices
 - [X] parallelise Monte Carlo simulations using multiprocessing
 - [X] Output as CSV
 - [ ] Visualise output
