from django.urls import path, include
from rest_framework import routers
from . import views 


# router = routers.DefaultRouter()
# router.register(r'',views.BookModel, basename='book-list')
urlpatterns = [
    # path('', include(router.urls)),
    path('', views.BookListCreateView.as_view(), name="book-list"),
    path('<slug:book_slug>', views.BookCreateRetrieveDeleteUpdateView.as_view(), name="book-details"),
]


