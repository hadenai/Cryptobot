from rest_framework import routers
from crypto_Bot.views.views import KlinesViewSet

router = routers.DefaultRouter()
router.register('klines-list', KlinesViewSet)