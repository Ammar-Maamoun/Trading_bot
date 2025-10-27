from ib_insync import IB, MarketOrder, Crypto, util
import pandas_ta as ta
from datetime import datetime
import time as t
import pandas as pd


# CONNECT TO IBKR PAPER ACCOUNT
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=4)
print(" Connected to IBKR Paper Account (Crypto Live Data)!")

# CRYPTO CONTRACTS

btc = Crypto('BTC', 'PAXOS', 'USD')
eth = Crypto('ETH', 'PAXOS', 'USD')
contracts = [btc, eth]

# Subscribe to live market data
for contract in contracts:
    ib.qualifyContracts(contract)
    ib.reqMktData(contract, '', False, False)
    print(f"Subscribed to live market data for {contract.symbol}")

#STRATEGY PARAMETERS

rsi_window = 14
unit_size = 0.001  # amount of crypto to trade per order
price_history = {contract.symbol: [] for contract in contracts}

#STRATEGY LOGIC
def calculate_rsi(prices, window=14):
    """Compute RSI using pandas_ta."""
    if len(prices) < window:
        return None
    s = pd.Series(prices)
    rsi_series = ta.rsi(s, length=window)
    if rsi_series.isna().all():
        return None
    return rsi_series.dropna().iloc[-1]

def should_buy(rsi):
    return rsi is not None and rsi < 30

def should_sell(rsi):
    return rsi is not None and rsi > 70

# MAIN LOOP (LIVE)
print("Starting live crypto trading with market data (BTC/USD, ETH/USD)")

while True:
    for contract in contracts:
        try:
            ticker = ib.ticker(contract)
            last_price = ticker.last or ticker.marketPrice()

            if last_price:
                prices = price_history[contract.symbol]
                prices.append(last_price)
                if len(prices) > 200:
                    prices.pop(0)

                rsi = calculate_rsi(prices, rsi_window)

                if rsi is not None:
                    print(f"{contract.symbol} → Price: {last_price:.2f} | RSI: {rsi:.2f}")

                    if should_buy(rsi):
                        print(f"BUY {contract.symbol} @ {last_price:.2f}")
                        ib.placeOrder(contract, MarketOrder('BUY', unit_size))

                    elif should_sell(rsi):
                        print(f" SELL {contract.symbol} @ {last_price:.2f}")
                        ib.placeOrder(contract, MarketOrder('SELL', unit_size))
                else:
                    print(f"{contract.symbol} → Waiting for more data...")

            else:
                print(f"No live tick yet for {contract.symbol}")

        except Exception as e:
            print(f"Error with {contract.symbol}: {e}")

    print("⏱ Cycle complete — checking again in 60s\n")
    t.sleep(60)

# DISCONNECT
ib.disconnect()
print(" Disconnected from IBKR.")
