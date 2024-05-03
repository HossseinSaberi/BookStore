from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from .manager import CustomManager
from django.utils.translation import gettext_lazy as _
from Core import models as CModel
from Core import utils as CUtils
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_IN_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    username = models.CharField(_("UserName"), max_length=50, unique=True)
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    phone_number = models.CharField(_("PhoneNumber"), max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_IN_CHOICES, null=True, blank=True)
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
