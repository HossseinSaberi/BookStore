from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from Core import paginations as cpage, views as cviews, mixins as cmixin
from . import models
from . import serializers

# Create your views here.


class BookListCreateView(
        cmixin.SerializerByMethodMixin,
        cmixin.CreateMixin,
        cmixin.ListMixin,
        cviews.BaseApiView
        ):

    model = models.Book
    queryset = model.objects.all()
    paginator_class = cpage.CustomPagination
    serializer_map = {
        'GET': serializers.BookListSerializer,
        'POST': serializers.BookDetailsSerializer,
    }

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookCreateRetrieveDeleteUpdateView(
        cmixin.UpdateMixin,
        cmixin.DeleteMixin,
        cmixin.RetrieveMixin,
        cviews.BaseApiView):
    
    model = models.Book
    queryset = model.objects.all()
    serializer_class = serializers.BookDetailsSerializer
    lookup_field = 'book_slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
