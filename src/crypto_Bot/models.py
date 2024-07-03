from django.db import models


class Klines(models.Model):
    open_time = models.FloatField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume_assets = models.FloatField()
    close_time = models.FloatField()
    volume_actif = models.FloatField()
    number_trades = models.FloatField()
    taker_buy_volume = models.FloatField()
    taker_buy_actif_volume = models.FloatField()
