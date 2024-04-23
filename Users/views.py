from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from Core import paginations as cpage, views as cviews, mixins as cmixin
from . import models
from . import serializers
# Create your views here.


class AuthorListCreateView(
        cviews.CreateListView
):
    model = models.Author
    queryset = model.objects.all()
    paginator_class = cpage.CustomPagination
    parser_classes = [MultiPartParser,]
    serializer_map = {
        'GET': serializers.AuthorListSerializer,
        'POST': serializers.AuthorDetailsSerializer,
    }
    
    
class AuthorRetrieveDeleteUpdateView(
        cviews.RetrieveDeleteUpdateView):

    model = models.Author
    queryset = model.objects.all()
    serializer_class = serializers.AuthorDetailsSerializer
    parser_classes = [MultiPartParser,]
    lookup_field = 'author_slug'

