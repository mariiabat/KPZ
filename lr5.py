import pandas as pd
from datetime import datetime, timedelta
from binance.client import Client
from pandas_ta import rsi, cci, macd, atr, adx

def fetch_data(asset: str, interval: str, days: int = 30) -> pd.DataFrame:
    """Fetch historical price data from Binance."""
    client = Client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    klines = client.get_historical_klines(
        asset,
        interval,
        start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time.strftime("%Y-%m-%d %H:%M:%S")
    )
    df = pd.DataFrame(klines, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df[['time', 'open', 'high', 'low', 'close', 'volume']]

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (RSI)."""
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_sma(df: pd.DataFrame, period: int) -> pd.Series:
    """Calculate Simple Moving Average (SMA)."""
    return df['close'].rolling(window=period).mean()

def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """Calculate Bollinger Bands."""
    sma = calculate_sma(df, period)
    std = df['close'].rolling(window=period).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return pd.DataFrame({'BBL': lower_band, 'BBM': sma, 'BBU': upper_band})

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Average True Range (ATR)."""
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate and add technical indicators to the DataFrame."""
    df['RSI'] = calculate_rsi(df)
    df['SMA_50'] = calculate_sma(df, 50)
    df['SMA_200'] = calculate_sma(df, 200)
    bb = calculate_bollinger_bands(df)
    df[['BBL', 'BBM', 'BBU']] = bb
    df['ATR'] = calculate_atr(df)
    return df

def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    """Save DataFrame to a CSV file."""
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Define parameters
    asset = "BTCUSDT"
    interval = Client.KLINE_INTERVAL_1HOUR
    # Calculate indicators
    df = fetch_data(asset, interval)
     # Save to CSV
    df = add_indicators(df)
    save_to_csv(df, "technical_analysis.csv")
    print(df.tail())
