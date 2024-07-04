from django.shortcuts import render
from rest_framework import viewsets

from crypto_Bot.models import Klines
from crypto_Bot.serializer import KlinesListSerializer
from crypto_Bot.ml_model import result_ml


def index(request):
    all_kines = Klines.objects.all()
    # Exécuter la fonction result_ml et récupérer son résultat
    result_ml_test = result_ml()
    return render(request, 'index.html', context={'all_kines': all_kines, 'result_ml_test': result_ml_test})


#expose sous forme d'api ma bdd
class KlinesViewSet(viewsets.ModelViewSet):
    queryset = Klines.objects.all()
    serializer_class = KlinesListSerializer
