from rest_framework import serializers
from .import models
from Users import serializers as USerializer, models as UModel


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
        fields = ['publisher_name']
        
class PublisherListSerializer(PublisherSerializer):
    pass
        
class PublisherDetailsSerializer(PublisherSerializer):
    class Meta:
        model = PublisherSerializer.Meta.model
        fields = PublisherSerializer.Meta.fields + \
            ['avatar'] 


### ================================================================ ###

class BookPublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookPublisher
        fields = '__all__'

### ================================================================ ###


class BaseBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ['book_name_en', 'book_name_fa',
                  'book_slug']


class BookListSerializer(BaseBookSerializer):
    author = USerializer.AuthorListSerializer(many=False, read_only=True)
    class Meta:
        model = BaseBookSerializer.Meta.model
        fields = BaseBookSerializer.Meta.fields + \
            ['author']  

class BookDetailsSerializer(BaseBookSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=UModel.Author.objects.all(),many=False)
    class Meta:
        model = BaseBookSerializer.Meta.model
        fields = BaseBookSerializer.Meta.fields + \
            ['short_description', 'writen_date' , 'author']  

### ================================================================ ###
