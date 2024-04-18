from rest_framework import serializers
from .import models

class BaseAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ['author_name','avatar']

class AuthorListSerializer(BaseAuthorSerializer):
    pass

class AuthorDetailsSerializer(BaseAuthorSerializer):
    pass