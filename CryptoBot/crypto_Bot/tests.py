from django.test import TestCase

from django.test import TestCase
from todo.models import Klines
from django.db.utils import IntegrityError

class KlinesTestCase(TestCase):  
  def test_create_kline(self):
    
    nb_kline_before = Klines.objects.count()
    
    new_kline = Klines()
    new_kline.open_time = 2.5
    new_kline.open_price = 2.5
    new_kline.high_price = 2.5
    new_kline.low_price = 2.5
    new_kline.close_price = 2.5
    new_kline.volume_assets = 2.5
    new_kline.close_time = 2.5
    new_kline.volume_actif = 2.5
    new_kline.number_trades = 2.5
    new_kline.taker_buy_volume = 2.5
    new_kline.taker_buy_actif_volume = 2.5
    
    
    new_kline.save()
    nb_kline_after = Klines.objects.count()
    self.assertTrue(nb_kline_before + 1 == nb_kline_after)

    new_kline.taker_buy_actif_volume = None
    with self.assertRaises(IntegrityError):
      new_kline.save()