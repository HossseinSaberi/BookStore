from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from Core import views as cview, paginations as cpage
from . import models
from . import serializers

# Create your views here.


class ListBook(cview.BaseModel):
    model = models.Book
    paginator_class = cpage.CustomPagination
    serializer_class = serializers.BookListSerializer

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        paginate_query_set = self.paginator_class().paginate_queryset(
            queryset=query_set, request=request)
        serializer = self.get_serializer(paginate_query_set, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class RetrieveBook(cview.BaseModel):
    model = models.Book
    serializer_class = serializers.BookDetailsSerializer
    lookup_field = None

    def retrieve(self, requests, *args, **kwargs):
        query_set = self.filter_queryset(kwargs)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)

