import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BYBIT_API_KEY')
API_SECRET = os.getenv('BYBIT_API_SECRET')
TESTNET = os.getenv('TESTNET', 'false').lower() == 'true'

SYMBOL_SPOT = os.getenv('SYMBOL_SPOT', 'PIPPIN/USDT')
SYMBOL_FUTURES = os.getenv('SYMBOL_FUTURES', 'PIPPINUSDT')
TIMEFRAME = os.getenv('TIMEFRAME', '1m')
LEVERAGE = int(os.getenv('LEVERAGE', 5))
POSITION_SIZE_USDT = float(os.getenv('POSITION_SIZE_USDT', 5.0))
TP_PCT = float(os.getenv('TP_PCT', 0.8))
SL_PCT = float(os.getenv('SL_PCT', 0.4))
RSI_BUY = int(os.getenv('RSI_BUY', 35))
RSI_SELL = int(os.getenv('RSI_SELL', 65))