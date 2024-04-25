from django.shortcuts import render
from rest_framework import viewsets

from crypto_Bot.models import Klines
from crypto_Bot.serializer import KlinesListSerializer
  
class KlinesViewSet(viewsets.ModelViewSet): 

  queryset = Klines.objects.all()
  serializer_class = KlinesListSerializer
