from models import Klines

# récupère tout les Klines de la bdd
data_klines = Klines.objects.all()
