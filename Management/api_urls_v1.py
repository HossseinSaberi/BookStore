from django.urls import path, include
from rest_framework import routers
from . import views 

urlpatterns = [
    path('', views.ObtainTokenView.as_view(), name="Token-Creation"),
    # path('', views.ObtainTokenView.as_view(), name="Token-Creation"),
]