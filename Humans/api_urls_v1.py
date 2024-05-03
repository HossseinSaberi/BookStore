from django.urls import path, include
from rest_framework import routers
from . import views 


# router = routers.DefaultRouter()
# router.register(r'',views.BookModel, basename='book-list')
urlpatterns = [
    # path('', include(router.urls)),
    path('author/', views.AuthorListCreateView.as_view(), name="author-list"),
    path('author/<slug:author_slug>', views.AuthorRetrieveDeleteUpdateView.as_view(), name="author-details"),
    
]
