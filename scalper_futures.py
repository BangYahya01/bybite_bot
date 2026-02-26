from config import *
import ccxt
import pandas as pd
import pandas_ta as ta
import time
from utils import logger

exchange = ccxt.bybit({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'},
})
if TESTNET:
    exchange.set_sandbox_mode(True)

exchange.set_leverage(LEVERAGE, SYMBOL_FUTURES)

def get_ohlcv():
    ohlcv = exchange.fetch_ohlcv(SYMBOL_FUTURES, TIMEFRAME, limit=100)
    df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
    return df

def indicators(df):
    df['ema5'] = ta.ema(df['c'], length=5)
    df['ema10'] = ta.ema(df['c'], length=10)
    df['rsi'] = ta.rsi(df['c'], length=14)
    return df

def signal(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if prev['ema5'] < prev['ema10'] and last['ema5'] > last['ema10'] and last['rsi'] < RSI_BUY:
        return 'buy'
    if prev['ema5'] > prev['ema10'] and last['ema5'] < last['ema10'] and last['rsi'] > RSI_SELL:
        return 'sell'
    return None

logger.info("Futures scalper started")

while True:
    try:
        df = get_ohlcv()
        df = indicators(df)
        sig = signal(df)
        if sig:
            price = df['c'].iloc[-1]
            side = 'buy' if sig == 'buy' else 'sell'
            amount = POSITION_SIZE_USDT / price * LEVERAGE
            logger.info(f"Sinyal {sig.upper()} @ ${price:.6f} | Qty {amount:.4f}")
            # Uncomment kalo live:
            # order = exchange.create_market_order(SYMBOL_FUTURES, side, amount)
            # logger.info(order)
        time.sleep(5)
    except Exception as e:
        logger.error(e)
        time.sleep(30)