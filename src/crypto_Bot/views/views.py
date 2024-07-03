from django.shortcuts import render
from rest_framework import viewsets

from crypto_Bot.models import Klines
from crypto_Bot.serializer import KlinesListSerializer

def index(request):
  return render(request, 'index.html')
class KlinesViewSet(viewsets.ModelViewSet): 

  queryset = Klines.objects.all()
  serializer_class = KlinesListSerializer

