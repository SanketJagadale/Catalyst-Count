
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField

#create user model here
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username = username,
            password = password,
        )
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        return super(UserProfile, self).save(*args, **kwargs)
