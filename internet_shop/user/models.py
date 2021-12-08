from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils.constants import EMAIL_FIELD, TEXT_FIELD, CHAR_FIELD
from utils.base_models import BaseModel


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


class Language(BaseModel):
    language_name = models.CharField(max_length=CHAR_FIELD)
    alias = models.CharField(max_length=CHAR_FIELD)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(max_length=CHAR_FIELD, null=True)
    last_name = models.CharField(max_length=CHAR_FIELD, null=True)
    email = models.EmailField(verbose_name="email", max_length=EMAIL_FIELD, null=True)
    phone = models.CharField(max_length=CHAR_FIELD, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_DEFAULT, default=None, null=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Comment(BaseModel):
    text = models.TextField(max_length=TEXT_FIELD)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_approved = models.BooleanField(default=False)
