from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from Core import models as CModel
from Core import utils as CUtils
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.

class WriterBase(models.Model):
    bio = models.TextField(_("bio"), null=True, blank=True)
    avatar = models.ImageField(
        default='Images/avatar.png', null=True, blank=True)

    class Meta:
        abstract = True


class Author(WriterBase):
    author_name_en = models.CharField(_("Author_Name_En"), max_length=50, blank=True, null=True)
    author_name_fa = models.CharField(_("Author_Name_Fa"), max_length=50, blank=True, null=True)
    author_slug = models.SlugField(
        _("Author_Slug"),  blank=True, null=True,allow_unicode=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.author_name_fa

    def get_absolute_url(self):
        return reverse("Author_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.author_slug:
            self.author_slug = slugify(self.author_name_en,allow_unicode=True)

        self.avatar.name = CUtils.change_image_name(
            self.avatar, self.__class__.__name__, self.author_name_en)

        super().save(*args, **kwargs)


class Translator(WriterBase):
    translator_name_en = models.CharField(
        _("Translator_Name_En"), max_length=50, null=True, blank=True)
    translator_name_fa = models.CharField(
        _("Translator_Name_Fa"), max_length=50, null=True, blank=True)
    translator_slug = models.SlugField(
        _("Translator_Slug"),  blank=True, null=True,allow_unicode=True)

    class Meta:
        verbose_name = _("Translator")
        verbose_name_plural = _("Translators")

    def __str__(self):
        return self.translator_name_fa

    def get_absolute_url(self):
        return reverse("Translator_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.translator_slug:
            self.translator_slug = slugify(self.translator_name_en,allow_unicode=True)

        self.avatar.name = CUtils.change_image_name(
            self.avatar, self.__class__.__name__, self.translator_name_en)
        super().save(*args, **kwargs)

