from django.urls import path, include
from rest_framework import routers
from . import views 


# router = routers.DefaultRouter()
# router.register(r'',views.BookModel, basename='book-list')
urlpatterns = [
    # path('', include(router.urls)),
    path('books/', views.BookListCreateView.as_view(), name="book-list"),
    path('books/<slug:book_slug>', views.BookRetrieveDeleteUpdateView.as_view(), name="book-details"),
    path('publisher/', views.PublisherListCreateView.as_view(), name="publisher-list"),
    path('publisher/<slug:publisher_slug>', views.PublisherRetrieveDeleteUpdateView.as_view(), name="publisher-details"),
    path('category/', views.CategoryListCreateView.as_view(), name="category-list"),
    path('category/<slug:category_slug>', views.CategoryRetrieveDeleteUpdateView.as_view(), name="category-details"),
    
]


