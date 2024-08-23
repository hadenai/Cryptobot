from decouple import config
from binance import Client
from crypto_Bot.serializer import KlinesListSerializer
from ..binance_api import BinanceAPI

api_key = config('API_KEY')
secret_key = config('SECRET_KEY')  

binance_api = BinanceAPI(api_key, secret_key, testnet=True)
#today au lieu d'une journée précise
klines = binance_api.get_first_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "20 Jun, 2023")
#klines = binance_api.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "20 Jun, 2023")
#print(klines)
#breakpoint()

for kline in klines:
  data_binance_klines = {
      'open_time': kline[0],
      'open_price': kline[1],
      'high_price': kline[2],
      'low_price': kline[3],
      'close_price': kline[4],
      'volume_assets': kline[5],
      'close_time': kline[6],
      'volume_actif': kline[7],
      'number_trades': kline[8],
      'taker_buy_volume': kline[9],
      'taker_buy_actif_volume': kline[10]
  }

  serializer = KlinesListSerializer(data=data_binance_klines)
  if serializer.is_valid():
      todo_instance = serializer.save()

  if not serializer.is_valid():
      print(serializer.errors)
