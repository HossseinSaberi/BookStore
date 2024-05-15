from django.db import models
from Core import models as CModel
from .manager import CouponManager
from django.conf import settings
from django.dispatch import Signal
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal
import random
from Books.models import BookPublisher


# Create your models here.


class Order(CModel.BaseClass):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    items = models.ManyToManyField('Books.BookPublisher', verbose_name=_("Order Item"), through='OrderItem')
    coupon = models.ForeignKey('Order.Coupon', verbose_name=_("Coupon"), on_delete=models.SET_NULL, blank=True,
                               null=True)

    @property
    def get_total_cost(self):
        try:
            total_cost = sum(item.get_item_total for item in self.orderitem_set.all())
            return self.coupon.apply_discount(total_cost)
        except Exception as e:
            print(e)

    def __str__(self):
        return '{} Order Number {}'.format(self.user.username, self.id)


class OrderItem(CModel.BaseClass):
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE)
    book_publisher = models.ForeignKey('Books.BookPublisher', verbose_name=_("Book Publisher"),
                                       on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    @property
    def get_item_total(self):
        generic_model = ContentType.objects.get_for_model(BookPublisher)
        discount = Discount.objects.filter(content_type=generic_model, object_id=self.book_publisher.pk)
        total_cost = sum(item.apply_discount(self.book_publisher.price) * self.quantity for item in discount)
        return total_cost

    def __str__(self):
        return '{} from {}'.format(self.book_publisher.book, self.book_publisher.publisher)


class BasicDiscount(CModel.BaseClass):
    discount_type = models.CharField(max_length=10, choices=settings.COUPON_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    # campaign = models.ForeignKey('Campaign', verbose_name=_("Campaign"), on_delete=models.CASCADE, blank=True,
    #                              null=True, related_name='coupons')

    def apply_discount(self, price):

        if self.discount_type == 'percentage':
            discount_price = price - (price * (self.discount_value / 100))
        elif self.discount_type == 'monetary':
            discount_price = price - self.discount_value
        else:
            discount_price = price

        assert discount_price > 0, 'Discount Price Can Not Be More Than Main Price!'
        return discount_price

    class Meta:
        abstract = True


class Discount(BasicDiscount):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type_discount')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return '{} with {}'.format(self.discount_type, self.discount_value)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Coupon(BasicDiscount):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type_coupon')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    coupon_code = models.CharField(
        _("Coupon Code"), max_length=30, unique=True,
        help_text=_("Leaving this field empty will generate a random code."), blank=True)
    user_limit = models.PositiveIntegerField(_("User limit"), default=1)
    valid_from = models.DateTimeField(
        _("Valid from"), default=timezone.now())
    valid_to = models.DateTimeField(
        _("Valid until"), blank=True, null=True,
        help_text=_("Leave empty for coupons that never expire"))


    objects = CouponManager()

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return '{} with {} with Code : {}'.format(self.discount_type, self.discount_value, self.coupon_code)

    def save(self, *args, **kwargs):
        if not self.coupon_code:
            self.coupon_code = Coupon.generate_code()
        super(Coupon, self).save(*args, **kwargs)

    def apply_discount(self , price):
        if not self.is_valid:
            self.discount_value = 0
            # raise Exception('Coupon Time is Gone!')
        return super().apply_discount(price)

    @property
    def is_redeemed(self):
        return self.users.filter(
            redeemed_at__isnull=False
        ).count() >= self.user_limit and self.user_limit != 0

    @property
    def redeemed_at(self):
        try:
            return self.users.filter(redeemed_at__isnull=False).order_by('redeemed_at').last().redeemed_at
        except self.users.through.DoesNotExist:
            return None

    @classmethod
    def generate_code(cls, prefix="", segmented=settings.SEGMENTED_CODES):
        code = "".join(random.choice(settings.CODE_CHARS) for i in range(settings.CODE_LENGTH))
        if segmented:
            code = settings.SEGMENT_SEPARATOR.join(
                [code[i:i + settings.SEGMENT_LENGTH] for i in range(0, len(code), settings.SEGMENT_LENGTH)])
            return prefix + code
        else:
            return prefix + code

    @property
    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to

    def redeem(self, user=None):
        try:
            coupon_user = self.users.get(user=user)
        except CouponUser.DoesNotExist:
            try:
                coupon_user = self.users.get(user__isnull=True)
                coupon_user.user = user
            except CouponUser.DoesNotExist:
                coupon_user = CouponUser(coupon=self, user=user)
        coupon_user.redeemed_at = timezone.now()
        coupon_user.save()


class Campaign(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __str__(self):
        return self.name


class CouponUser(models.Model):
    coupon = models.ForeignKey(Coupon, related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), null=True, blank=True,
                             on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(_("Redeemed at"), blank=True, null=True)

    class Meta:
        unique_together = (('coupon', 'user'),)

    def __str__(self):
        return str(self.user)
