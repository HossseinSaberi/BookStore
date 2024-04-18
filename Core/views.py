from rest_framework import viewsets


class BaseModel(viewsets.ViewSet):
    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all()

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
    def filter_queryset(self, kwargs):
        return self.get_queryset().filter(**kwargs)
    