from django.contrib import admin
from .models import Order, OrderItem, Discount, Coupon, Campaign, CouponUser
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('pk', 'book_publisher'), ('quantity', 'get_item_total'),)
        },),)
    readonly_fields = ('get_item_total','pk')


class CouponAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('coupon_code', 'discount_type', 'discount_value'), ('valid_from', 'valid_to', 'user_limit'),
                       ('content_type', 'object_id'), ('campaign',),)
        },),)


class OrderAdmin(admin.ModelAdmin):
    # list_display = ("user",)
    list_filter = ("user__username",)
    fieldsets = (
        ('Main Detail', {
            'classes': ('wide',),
            'fields': (('user', 'coupon'), ('get_total_cost',)), },),)
    readonly_fields = ('get_total_cost',)

    inlines = [OrderItemInline, ]


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount)
admin.site.register(Coupon, CouponAdmin)
# admin.site.register(Campaign)
admin.site.register(CouponUser)
