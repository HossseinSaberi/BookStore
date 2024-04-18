from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from .utils import get_upload_path

# Create your models here.
class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True
        
    
        
class Image(BaseClass):

    image = models.ImageField()
    content_type = models.ForeignKey(ContentType, verbose_name=_(""), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return 'image for {}'.format(self.content_object)

    
    def save(self, *args, **kwargs):
        old_file_name , file_ext = self.image.name.rsplit('.',1)
        self.image.name = get_upload_path(self.content_type.model, self.object_id, file_ext)
        super().save(*args, **kwargs)
