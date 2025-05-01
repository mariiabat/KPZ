import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def calculate_rsi(asset: str, periods: list) -> pd.DataFrame:
"""Visualize RSI data from CSV file using different plot types"""
 client = Client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    klines = client.get_historical_klines(
        asset,
        Client.KLINE_INTERVAL_1MINUTE,
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
    for period in periods:
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        loss.replace(0, float('nan'), inplace=True)
        rs = gain / loss
        df[f'RSI_{period}'] = 100 - (100 / (1 + rs))
    return df[['time', 'open', 'close'] + [f'RSI_{p}' for p in periods]]
if __name__ == "__main__":
    asset = "BTCUSDT"
    periods = [14, 27, 100]
    rsi_data = calculate_rsi(asset, periods)
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    graph_types = ['plot', 'scatter', 'bar']
    for i, (period, ax, gtype) in enumerate(zip(periods, axs, graph_types)):
        if gtype == 'plot':
            ax.plot(rsi_data['time'], rsi_data[f'RSI_{period}'])
        elif gtype == 'scatter':
            ax.scatter(rsi_data['time'], rsi_data[f'RSI_{period}'], s=5)
        elif gtype == 'bar':
            ax.bar(rsi_data['time'], rsi_data[f'RSI_{period}'], width=0.001)
        ax.set_title(f'{gtype} - RSI {period}')
        ax.set_ylabel('RSI')
    axs[-1].set_xlabel('Time')
    plt.tight_layout()
    plt.savefig('rsi_visualization.png')
    plt.show()
