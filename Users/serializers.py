from rest_framework import serializers
from .import models

class BaseAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ['author_name',]

class AuthorListSerializer(BaseAuthorSerializer):
    pass

class AuthorDetailsSerializer(BaseAuthorSerializer):
    class Meta:
        model = BaseAuthorSerializer.Meta.model
        fields = BaseAuthorSerializer.Meta.fields + ['avatar']