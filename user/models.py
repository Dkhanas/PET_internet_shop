import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from PET_internet_shop.settings import *


class BaseClass(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, username, password):

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseClass):
    username = models.CharField(max_length=USER_MODELS_MAX_LENGTH['EmailField'], unique=True, default="")
    first_name = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])
    last_name = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])
    email = models.EmailField(verbose_name="email", max_length=USER_MODELS_MAX_LENGTH['EmailField'], unique=True)
    phone = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Language(BaseClass):
    language_name = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'], default="")
    alias = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])


class Comment(BaseClass):
    text = models.TextField(max_length=USER_MODELS_MAX_LENGTH['TextField'])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_approved = models.BooleanField(default=False)
