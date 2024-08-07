"""
URL configuration for CryptoBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
