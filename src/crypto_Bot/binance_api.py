from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager


class BinanceAPI:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)

    def get_historical_klines(self, symbol, interval, date):
        return self.client.get_historical_klines(symbol, interval, date)

    def get_first_klines(self, symbol, interval, date, limit=10):
        klines = self.get_historical_klines(symbol, interval, date)
        return klines[:limit]
