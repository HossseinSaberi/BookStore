from django.urls import path, include
from rest_framework import routers
from . import views 


# router = routers.DefaultRouter()
# router.register(r'',views.BookModel, basename='book-list')

urlpatterns = [
    path('v1/', include('Books.api_urls_v1'), name='books'),
    path('v1/human/', include('Humans.api_urls_v1'), name='writers'),
    path('v1/token/', include('Management.api_urls_v1'), name='users'),
]



