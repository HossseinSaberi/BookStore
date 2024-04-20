from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from Core import paginations as cpage, views as cviews, mixins as cmixin
from . import models
from . import serializers

## ====================================Books=====================================##


class BookListCreateView(
        cviews.CreateListView
):

    model = models.Book
    queryset = model.objects.all()
    paginator_class = cpage.CustomPagination
    serializer_map = {
        'GET': serializers.BookListSerializer,
        'POST': serializers.BookDetailsSerializer,
    }


class BookRetrieveDeleteUpdateView(
        cviews.RetrieveDeleteUpdateView):

    model = models.Book
    queryset = model.objects.all()
    serializer_class = serializers.BookDetailsSerializer
    lookup_field = 'book_slug'


## ==============================================================================##

## ==================================Publisher===================================##

class PublisherListCreateView(
        cviews.CreateListView
):
    model = models.Publisher
    queryset = model.objects.all()
    paginator_class = cpage.CustomPagination
    parser_classes = [MultiPartParser,]
    serializer_map = {
        'GET': serializers.PublisherListSerializer,
        'POST': serializers.PublisherDetailsSerializer,
    }


class PublisherRetrieveDeleteUpdateView(
        cviews.RetrieveDeleteUpdateView):

    model = models.Publisher
    queryset = model.objects.prefetch_related('book_set')
    serializer_class = serializers.PublisherDetailsSerializer
    parser_classes = [MultiPartParser,]
    lookup_field = 'publisher_slug'
    
    def get(self, request, *args, **kwargs):
        publisher = self.get_object()
        serializer = serializers.PublisherBooksSerializer(publisher)
        return Response(serializer.data)


## =============================================================================##

## ==================================Category===================================##

class CategoryListCreateView(
        cviews.CreateListView
):
    model = models.Category
    queryset = model.objects.all()
    paginator_class = cpage.CustomPagination
    parser_classes = [MultiPartParser,]
    serializer_map = {
        'GET': serializers.CategoryListSerializer,
        'POST': serializers.CategoryDetailsSerializer,
    }


class CategoryRetrieveDeleteUpdateView(
        cviews.RetrieveDeleteUpdateView):

    model = models.Category
    queryset = model.objects.prefetch_related('book_set')
    serializer_class = serializers.CategoryDetailsSerializer
    parser_classes = [MultiPartParser,]
    lookup_field = 'category_slug'
    
    
    def get(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = serializers.CategoryBooksSerializer(category)
        return Response(serializer.data)