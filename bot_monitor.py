from config import API_KEY, API_SECRET, TESTNET, SYMBOL_SPOT
import ccxt
import time
from utils import logger

exchange = ccxt.bybit({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'},
})
if TESTNET:
    exchange.set_sandbox_mode(True)

logger.info("Monitor started")

try:
    balance = exchange.fetch_balance()
    usdt = balance.get('USDT', {}).get('free', 0)
    logger.info(f"USDT free: ${usdt:.2f}")
except Exception as e:
    logger.error(e)

while True:
    try:
        ticker = exchange.fetch_ticker(SYMBOL_SPOT)
        logger.info(f"{SYMBOL_SPOT} ${ticker['last']:.6f} | {ticker['percentage']:.2f}%")
    except Exception as e:
        logger.error(e)
    time.sleep(10)