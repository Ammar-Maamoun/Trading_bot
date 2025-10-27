


 Live Crypto RSI Trading Bot (IBKR Integration)

 Overview

This script connects to an Interactive Brokers (IBKR) paper account to receive live cryptocurrency market data and execute trades automatically based on a Relative Strength Index (RSI) strategy.

It demonstrates realtime data handling, trading logic, and basic algorithmic execution using Python and the ib_insync library.



 Features

 Connects securely to IBKR Paper Trading API.
 Subscribes to live BTC/USD and ETH/USD price feeds.
 Calculates RSI (Relative Strength Index) in real time using `pandas_ta`.
 Executes market buy/sell orders based on RSI thresholds:

   Buy when RSI < 30
   Sell when RSI > 70
 Maintains a rolling price history for each crypto symbol.
 Designed for continuous operation with cycle intervals.



 Requirements

 Python 3.8+
 Installed libraries:

  ```bash
  pip install ib_insync pandas pandas_ta
  ```
 Active IBKR Paper Trading account with TWS or IB Gateway running.



 Configuration

Before running:

1. Make sure IB Gateway or Trader Workstation (TWS) is running on your machine.
2. Enable API access (usually at `127.0.0.1` and port `4002` for paper trading).
3. Adjust the following parameters in the script if needed:

   ```python
   rsi_window = 14
   unit_size = 0.001
   ```
4. You can add more crypto pairs by extending:

   ```python
   contracts = [btc, eth]
   ```



 How It Works

1. Connects to IBKR via `ib.connect('127.0.0.1', 4002, clientId=4)`.
2. Subscribes to live data for BTC/USD and ETH/USD.
3. Continuously updates price history and computes RSI.
4. Places market buy/sell orders when RSI signals oversold or overbought conditions.
5. Waits 60 seconds between each trading cycle.





