from rest_framework import serializers
from .import models
from Humans import serializers as USerializer, models as UModel


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['title', 'category_slug']


class CategoryListSerializer(BaseCategorySerializer):
    pass


class CategoryDetailsSerializer(BaseCategorySerializer):
    class Meta:
        model = BaseCategorySerializer.Meta.model
        fields = BaseCategorySerializer.Meta.fields + \
            ['bio', 'parent', 'logo']

### ================================================================ ###


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = ['publisher_name','publisher_slug']


class PublisherListSerializer(PublisherSerializer):
    pass


class PublisherDetailsSerializer(PublisherSerializer):
    class Meta:
        model = PublisherSerializer.Meta.model
        fields = PublisherSerializer.Meta.fields + \
            ['avatar']


### ================================================================ ###

class BookPublisherSerializer(serializers.ModelSerializer):

    publisher = PublisherListSerializer()

    class Meta:
        model = models.BookPublisher
        fields = ['publisher', 'translator', 'isbn',
                  'price', 'edition_series', 'publisher_data']


class BookCategorySerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = models.BookCategory
        fields = ['category', 'short_description']


### ================================================================ ###


class BaseBookSerializer(serializers.HyperlinkedModelSerializer):
    author = USerializer.AuthorListSerializer(many=False, read_only=True)
    class Meta:
        model = models.Book
        fields = ['book_name_en', 'book_name_fa',
                  'book_slug', 'author']


class BookListSerializer(BaseBookSerializer):
    pass


class BookDetailsSerializer(BaseBookSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='author-details',
        lookup_field='author_slug',
        read_only=True
    )

    publishers = BookPublisherSerializer(
        many=True, source='bookpublisher_set', read_only=True)
    categories = BookCategorySerializer(
        many=True, source='bookcategory_set', read_only=True)

    class Meta:
        model = BaseBookSerializer.Meta.model
        fields = BaseBookSerializer.Meta.fields + \
            ['short_description', 'writen_date', 'publishers', 'categories']

### ================================================================ ###


class PublisherBooksSerializer(serializers.ModelSerializer):
    book_set = BookListSerializer(many=True)

    class Meta:
        model = models.Publisher
        fields = ['publisher_name', 'publisher_slug', 'avatar', 'book_set']


class CategoryBooksSerializer(serializers.ModelSerializer):
    book_set = BookListSerializer(many=True)

    class Meta:
        model = models.Category
        fields = ['title', 'category_slug',
                  'bio', 'parent', 'logo', 'book_set']
