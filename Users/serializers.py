from rest_framework import serializers
from django.utils.module_loading import import_string
from .import models

class BaseAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Author
        fields = ['author_name_en','author_name_fa']

class AuthorListSerializer(BaseAuthorSerializer):
    pass

class AuthorDetailsSerializer(BaseAuthorSerializer):
    author_books = serializers.SerializerMethodField()
    class Meta:
        model = BaseAuthorSerializer.Meta.model
        fields = BaseAuthorSerializer.Meta.fields + ['avatar', 'bio', 'author_books']
        depth = 1
        
    def get_author_books(self, obj):
        BookSerializer = import_string('Books.serializers.BookListSerializer')
        books = obj.book_author.all()
        return BookSerializer(books, many=True, context=self.context).data
        
        
    