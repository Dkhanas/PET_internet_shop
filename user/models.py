import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from PET_internet_shop.settings import *


class BaseClass(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError("User must have username")
        if not phone:
            raise ValueError("User must have phone number")
        if not first_name:
            raise ValueError("User must have first name")
        if not last_name:
            raise ValueError("User must have last name")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseClass):
    email = models.EmailField(verbose_name="email", max_length=USER_MODELS_MAX_LENGTH['EmailField'], unique=True)
    first_name = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])
    last_name = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])
    phone = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserManager()


class Language(BaseClass):
    language_name = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'], default="")
    alias = models.CharField(max_length=USER_MODELS_MAX_LENGTH['CharField'])


class Comment(BaseClass):
    text = models.TextField(max_length=USER_MODELS_MAX_LENGTH['TextField'])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_approved = models.BooleanField(default=False)
