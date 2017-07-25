# KrakenBot
(WIP) Crypto trading bot for the Kraken exchange.

Dependant on the krakenex Python API wrapper: https://github.com/veox/python3-krakenex

*** Live trading has not yet been tested ***

Supports any asset pair on the Kraken exchange. Multiple instances of the program can be used to trade multiple asset pairs at the same time (though care should be given not to go above the API call limit). Only one time frame per asset pair is supported (e.g. 5m charts). 

Features:
- Automated data importing and exporting
- Automated BUY / SELL market orders based on the simple moving average crossover strategy
- Monte Carlo simulation in order to determine most profitable SMA parameters over a given set of data

To-do:
- New BUY / SELL indicators and strategies (e.g. EMA crossover)
- Analysis of executed trades and comparison to expected outcome (e.g. order failures, slippage, actual profits after commission, etc)
- Circuit break functionality if there are too many losing trades in a row
- E-mail alerts
- General code optimisation
