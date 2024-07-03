from rest_framework import serializers
from crypto_Bot.models import Klines
    
class KlinesListSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Klines
    fields = '__all__'