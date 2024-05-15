from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from Core import models as CModel


# Create your models here.


class Like(CModel.BaseClass):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liker')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type_liker')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return '{} liked {}'.format(self.user, self.content_object)


class Comment(CModel.BaseClass):
    content = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commenter')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type_comment')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.user} Commented on {self.content_object}"


class WishList(CModel.BaseClass):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wisher')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type_wisher')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("WishList")
        verbose_name_plural = _("WishList")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return '{} added {} to WishList'.format(self.user, self.content_object)
