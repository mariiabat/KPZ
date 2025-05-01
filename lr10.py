import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client

# Клас Trade
class Trade:
    def __init__(self, entry_price, sl, tp, entry_time):
        self.entry_price = entry_price
        self.sl = sl
        self.tp = tp
        self.entry_time = entry_time
        self.exit_price = None
        self.exit_time = None
        self.result = None  

    def close(self, exit_price, exit_time, result):
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.result = result
def rsi(close_prices, period=14):
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
class Strategy:
    def should_enter(self, candles, index):
        raise NotImplementedError

    def should_exit(self, trade, candle):
        raise NotImplementedError

class RSIStrategy(Strategy):
    def should_enter(self, candles, index):
        if index < 100:
            return False
        rsi_series = rsi(candles["close"], 14)
        current_rsi = rsi_series.iloc[-1]
        return current_rsi < 30  # Вхід при перепроданості

    def should_exit(self, trade, candle):
        return candle["low"] < trade.sl or candle["high"] > trade.tp

# Головний клас Backtester
class Backtester:
    def __init__(self, data, tp=50, sl=20, initial_amount=1000):
        self.data = data.reset_index(drop=True)
        self.tp = tp
        self.sl = sl
        self.amount = initial_amount
        self.initial_amount = initial_amount
        self.trades = []
        self.strategy = RSIStrategy()

    def run(self):
        print("Running backtest...")
        for index, candle in enumerate(self.data[100:-1], start=100):
            last_candles = self.data.iloc[index - 100: index]

            if self.strategy.should_enter(last_candles, index):
                entry_price = candle["close"]
                sl = entry_price - self.sl
                tp = entry_price + self.tp
                trade = Trade(entry_price, sl, tp, candle["time"])
                self.trades.append(trade)

            for trade in self.trades:
                if trade.exit_price is None:  # Open trade
                    if candle["low"] < trade.sl:
                        trade.close(trade.sl, candle["time"], "loss")
                    elif candle["high"] > trade.tp:
                        trade.close(trade.tp, candle["time"], "win")

    def report(self):
        total = len([t for t in self.trades if t.exit_price is not None])
        wins = sum(1 for t in self.trades if t.result == "win")
        losses = total - wins
        pnl = sum((t.exit_price - t.entry_price) if t.result == "win"
                  else (t.exit_price - t.entry_price)
                  for t in self.trades if t.exit_price is not None)

        print("===== Backtest Report =====")
        print(f"Total Trades: {total}")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        if total > 0:
            print(f"Win Rate: {wins / total * 100:.2f}%")
        print(f"PnL: {pnl:.2f}")
        print(f"Net Profit: {self.amount + pnl - self.initial_amount:.2f}")

# Запуск 
if __name__ == "__main__":
    # Завантаження CSV: time, open, high, low, close
    data = pd.read_csv("data.csv")
    backtester = Backtester(data, tp=50, sl=20, initial_amount=1000)
    backtester.run()
    backtester.report()
