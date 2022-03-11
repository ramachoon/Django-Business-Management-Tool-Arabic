from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_avatar
from src.extensions.upload_file_path import upload_path


# Create your models here.
class User(AbstractUser):
    """
    Customize user model.
    """

    bio = models.TextField(default='بیوگرافی خودرا ویرایش کنید', verbose_name='بیوگرافی')
    avatar = models.ImageField(
        upload_to=upload_path('accounts/avatars'), default='default.jpg', validators=[validate_avatar], verbose_name='avatar'
    )
    is_employee = models.BooleanField(default=False, verbose_name='کارمند')
    is_customer = models.BooleanField(default=False, verbose_name='کارفرما')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_supporter = models.BooleanField(default=False, verbose_name='پشتیبان')
