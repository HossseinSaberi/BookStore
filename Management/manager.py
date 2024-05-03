from django.contrib.auth.models import BaseUserManager


class CustomManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users Must Have an Email!')
        if not username:
            raise ValueError('User Must Have a UserName!')

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_account_enable = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def is_super_user(self, username):
        try:
            user = self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            return None
        if user.is_superuser:
            return True
        return False