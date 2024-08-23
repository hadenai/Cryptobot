from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from crypto_Bot.urls import router as crypto_router
from crypto_Bot.views import index

router = routers.DefaultRouter()
router.registry.extend(crypto_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('result', index, name="index")
]
