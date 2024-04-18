from django.urls import path, include
from rest_framework import routers
from . import views 


router = routers.DefaultRouter()
router.register(r'',views.ListBook, basename='book-list')
router.register(r'<book_slug>',views.RetrieveBook, basename='book-detail')
urlpatterns = [
    path('', include(router.urls)),
]


