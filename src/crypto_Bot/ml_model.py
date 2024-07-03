from crypto_Bot.models import Klines


def result_ml():
    # récupère tout les Klines de la bdd
    data_klines = Klines.objects.all()
    return "result Beautifull ml"
