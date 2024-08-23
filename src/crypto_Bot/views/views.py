from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

from crypto_Bot.models import Klines
from crypto_Bot.serializer import KlinesListSerializer
from crypto_Bot.ml_model import result_ml


from django.shortcuts import render

def index(request):
    if request.method == "POST":
        # Récupère les données du formulaire
        model_choice = request.POST.get('model_choice')
        interval_min = request.POST.get('interval_min')
        candlestick_count = request.POST.get('candlestick_count')

        # Vérifie si toutes les données sont présentes
        if model_choice and interval_min and candlestick_count:
            # Appeler la fonction ML avec les trois paramètres
            result = result_ml(model_choice, interval_min, candlestick_count)
            return render(request, 'index.html', {})
        else:
            return render(request, 'index.html', {'error': 'Please fill out all fields.'})
    else:
        return render(request, 'index.html')



#expose sous forme d'api ma bdd
class KlinesViewSet(viewsets.ModelViewSet):
    queryset = Klines.objects.all()
    serializer_class = KlinesListSerializer
