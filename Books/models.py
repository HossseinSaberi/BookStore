from django.db import models
from Core import models as CModel
from Core import utils as CUtils
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# Create your models here.


class Book(CModel.BaseClass):
    book_name_en = models.CharField(
        _("Book_Name"), max_length=100, null=True, blank=True)
    book_name_fa = models.CharField(
        _("Book_Name_Fa"), max_length=100, null=True, blank=True)
    book_slug = models.SlugField(_("Book_Slug"), blank=True, null=True)
    short_description = models.TextField(
        _("Book_Description"), null=True, blank=True)
    author = models.ForeignKey("Users.Author", verbose_name=_(
        "Author"), on_delete=models.PROTECT, related_name='book_author')
    publisher = models.ManyToManyField(
        "Books.Publisher", verbose_name=_("Publisher"), through='BookPublisher')
    category = models.ManyToManyField(
        "Books.Category", verbose_name=_("Category"), through='BookCategory')
    writen_date = models.IntegerField(_("Writen_Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return '{} from {}'.format(self.book_name_fa, self.author.author_name)

    def get_absolute_url(self):
        return reverse("Book_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.book_slug = slugify(self.book_name_en)
        super().save(*args, **kwargs)


class Publisher(models.Model):

    publisher_name = models.CharField(_("Publisher_Name"), max_length=50)
    publisher_slug = models.SlugField(
        _("Publisher_Slug"),  blank=True, null=True)
    avatar = models.ImageField(default='Images/avatar.png')

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")

    def __str__(self):
        return self.publisher_name

    def get_absolute_url(self):
        return reverse("Publisher_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.publisher_slug = slugify(self.publisher_name)
        self.avatar.name = CUtils.change_image_name(
            self.avatar, self.__class__.__name__, self.publisher_name)
        super().save(*args, **kwargs)


class BookShape(CModel.BaseClass):
    cover_type = models.CharField(_("Cover_Type"), max_length=50)
    size_type = models.CharField(_("Size_Type"), max_length=50)
    page_no = models.IntegerField(_("Page_Number"))
    main_image = models.ImageField(default='avatar.png')

    class Meta:
        abstract = True


class BookPublisher(BookShape):

    book = models.ForeignKey("Books.Book", on_delete=models.DO_NOTHING, null=True, blank=True)
    publisher = models.ForeignKey(
        "Books.Publisher", on_delete=models.DO_NOTHING, null=True, blank=True)
    translator = models.ForeignKey("Users.Translator", verbose_name=_(
        "Translator"), on_delete=models.SET_NULL, null=True, blank=True, related_name='book_translator')
    isbn = models.CharField(_("ISBN"), max_length=50)
    price = models.DecimalField(_("Price"), max_digits=15, decimal_places=0)
    edition_series = models.IntegerField(_("Edition_Series"))
    publisher_data = models.IntegerField(
        _("Publish_Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("BookPublisher")
        verbose_name_plural = _("BookPublishers")

    def __str__(self):
        return self.book.book_name_en

    def get_absolute_url(self):
        return reverse("BookPublisher_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        old_file_name, file_ext = self.main_image.name.rsplit('.', 1)
        self.main_image.name = CUtils.get_upload_path(
            'Book', self.book.book_name_en, file_ext)
        super().save(*args, **kwargs)


class Category(models.Model):

    title = models.CharField(_("Category"), max_length=50)
    bio = models.TextField(_("Category Description"), null=True, blank=True)
    category_slug = models.SlugField(_("Category_Slug"), blank=True, null=True)
    is_prize = models.BooleanField(_("Is_Prize"), default=False)
    logo = models.ImageField(default='Images/avatar.png')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.logo.name = CUtils.change_image_name(
            self.logo, self.__class__.__name__, self.title)
        self.category_slug = slugify(self.title)
        super().save(*args, **kwargs)

class BookCategory(models.Model):

    book = models.ForeignKey("Books.Book", on_delete=models.DO_NOTHING)
    category = models.ForeignKey(
        "Books.Category", on_delete=models.DO_NOTHING, null=True, blank=True)
    year = models.IntegerField(_("Year"),null=True, blank=True)
    short_description = models.CharField(
        _("book_prize_description"), max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _("BookCategory")
        verbose_name_plural = _("BookCategorys")

    def __str__(self):
        return self.category.title

    def get_absolute_url(self):
        return reverse("BookCategory_detail", kwargs={"pk": self.pk})
