from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class BaseCustomBackend(BaseBackend):
    def authenticate(self, request, username , has_password, password=None):
        user_data = {self.user_identifier: username}
        try:
            user = User.objects.get(**user_data)
            if (has_password is False) or (user.check_password(password) is True):
                return user
        except User.DoesNotExist:
            return None


class EmailModelBackend(BaseCustomBackend):
    user_identifier = 'email'


class UserNameModelBackend(BaseCustomBackend):
    user_identifier = 'username'


class MobileModelBackend(BaseCustomBackend):
    user_identifier = 'phone_number'
