from rest_framework import serializers
from .import models
from Users import serializers as USerializer


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['title', 'is_prize']


class CategoryListSerializer(BaseCategorySerializer):
    pass


class CategoryDetailsSerializer(BaseCategorySerializer):
    class Meta:
        fields = BaseCategorySerializer.Meta.fields + \
            ['bio', 'category_slug', 'logo']

### ================================================================ ###


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = ['publisher_name', 'avatar']


### ================================================================ ###


class BaseBookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(many=True, read_only=True)
    category = CategoryListSerializer(many=True, read_only=True)
    author = USerializer.AuthorListSerializer(many=False, read_only=True)

    class Meta:
        model = models.Book
        fields = ['book_name_en', 'book_name_fa',
                  'book_slug', 'author', 'publisher', 'category']


class BookListSerializer(BaseBookSerializer):
    pass


class BookDetailsSerializer(BaseBookSerializer):
    class Meta:
        model = BaseBookSerializer.Meta.model
        fields = BaseBookSerializer.Meta.fields + \
            ['short_description', 'writen_date'] #, 'category__title',
        # lookup_field = 'slug'
            
            
### ================================================================ ###
