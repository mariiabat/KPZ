import pandas as pd
import pandas_ta as ta
import numpy as np
from dataclasses import dataclass
from datetime import datetime, timedelta
import time
@dataclass
class Signal:
    time: datetime
    asset: str
    quantity: float
    side: str
    entry: float
    take_profit: float
    stop_loss: float
    result: str = "Proceed"
class Strategy:
    def __init__(self, asset: str, quantity: float = 1.0):
        self.asset = asset
        self.quantity = quantity
    def generate_fake_data(self) -> pd.DataFrame:
        times = pd.date_range(datetime.now() - timedelta(minutes=99), periods=100, freq='min')
        prices = np.cumsum(np.random.normal(0, 0.5, size=100)) + 100
        df = pd.DataFrame({'time': times, 'close': prices})
        df['high'] = df['close'] + np.random.rand(100)
        df['low'] = df['close'] - np.random.rand(100)
        df['open'] = df['close'] + np.random.uniform(-1, 1, size=100)
        return df
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df['EMA_14'] = df['close'].ewm(span=14).mean()
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        high = df['high']
        low = df['low']
        close = df['close']
        df['TR'] = np.maximum(high - low, np.maximum(abs(high - close.shift()), abs(low - close.shift())))
        df['ATR'] = df['TR'].rolling(window=14).mean()
        df['+DM'] = np.where((high - high.shift()) > (low.shift() - low), high - high.shift(), 0)
        df['-DM'] = np.where((low.shift() - low) > (high - high.shift()), low.shift() - low, 0)
        df['+DI'] = 100 * (df['+DM'].rolling(window=14).mean() / df['ATR'])
        df['-DI'] = 100 * (df['-DM'].rolling(window=14).mean() / df['ATR'])
        df['ADX'] = abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']) * 100
        return df
    def create_signal(self, df: pd.DataFrame) -> Signal | None:
        df = self.calculate_indicators(df)
        current = df.iloc[-1]
        price = current['close']
        rsi = current['RSI']
        adx = current['ADX']
        ema = current['EMA_14']
        side = None
        if rsi > 70 and price > ema:
            side = "SELL"
        elif rsi < 30 and price < ema:
            side = "BUY"
        if side and adx > 35:
            take_profit = round(price * 1.05 if side == "BUY" else price * 0.95, 2)
            stop_loss = round(price * 0.98 if side == "BUY" else price * 1.02, 2)
            return Signal(datetime.now(), self.asset, self.quantity, side, price, take_profit, stop_loss)
        return None
def monitor(strategy: Strategy):
    while True:
        df = strategy.generate_fake_data()
        signal = strategy.create_signal(df)
        if signal:
            print(f"[{signal.time}] SIGNAL: {signal.side} {signal.asset} @ {signal.entry}")
            print(f"  TP: {signal.take_profit}, SL: {signal.stop_loss}")
        else:
            print(f"[{datetime.now()}] No signal.")
        time.sleep(5)
if __name__ == "__main__":
    strategy = Strategy("coin_result", quantity=1.0)
    monitor(strategy)
