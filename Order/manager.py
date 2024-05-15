from django.db import models, IntegrityError
from django.utils import timezone


class CouponManager(models.Manager):
    def create_coupon(self, coupon_type, coupon_value, users=(), valid_to=None, valid_from=None, prefix="",
                      campaign=None, user_limit=None):
        coupon = self.create(
            discount_value=coupon_value,
            coupon_code=self.model.generate_code(prefix),
            discount_type=coupon_type,
            valid_to=valid_to,
            valid_from=valid_from,
            campaign=campaign,
        )
        if user_limit is not None:  # otherwise use default value of model
            coupon.user_limit = user_limit
        try:
            coupon.save()
        except IntegrityError:
            coupon = self.model.objects.create_coupon(coupon_type, coupon_value, users, valid_to, valid_from, prefix,
                                                      campaign)

        if not isinstance(users, tuple):
            users = [users]
        for user in users:
            self.model.users(user=user, coupon=coupon).save()

        return coupon

    def create_coupons(self, quantity, discount_type, discount_value, valid_to=None, valid_from=None, prefix="",
                       campaign=None):
        coupons = []
        for i in range(quantity):
            coupons.append(
                self.create_coupon(discount_type, discount_value, None, valid_to, valid_from, prefix, campaign))
        return coupons


    def used(self):
        return self.exclude(users__redeemed_at__isnull=True)

    def unused(self):
        return self.filter(users__redeemed_at__isnull=True)

    def expired(self):
        return self.filter(valid_until__lt=timezone.now())


