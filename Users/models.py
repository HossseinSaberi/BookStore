from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from Core import models as CModel
from Core import utils as CUtils
from .manager import CustomManager
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_("UserName"), max_length=50, unique=True)
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    phone_number = models.CharField(_("PhoneNumber"), max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_modify = models.DateTimeField(auto_now=True, editable=False)
    is_account_enable = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomManager()

    class Meta:
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("CustomUser_detail", kwargs={"pk": self.pk})


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


class Profile(CModel.BaseClass):

    firstname = models.CharField(max_length=30, verbose_name=_('FirstName'))
    lastname = models.CharField(max_length=30, verbose_name=_('LastName'))
    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(140), MinValueValidator(5)])
    avatar = models.ImageField(default='Images/avatar.png')
    bio = models.TextField()
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile_owner')

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Profile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        old_file_name, file_ext = self.avatar.name.rsplit('.', 1)
        self.avatar.name = CUtils.get_upload_path(
            self.__class__.__name__, self.user.username, file_ext)
        super().save(*args, **kwargs)


class Address(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('AddressName'))
    address_detail = models.TextField()
    zip_code = models.BigIntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_address', null=True, blank=True)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return "{} 's {} Address".format(self.profile.user.username, self.name)


class UserLastActivity(CModel.BaseClass):
    user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='activitor')
    action = models.CharField(max_length=50)
    user_agent = models.TextField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = _('User Last Activity')
        verbose_name_plural = _('Users Last Activity')

    def __str__(self):
        return f"{self.user} last activity"
