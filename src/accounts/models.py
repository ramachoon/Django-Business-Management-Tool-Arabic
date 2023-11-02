import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_avatar

from extensions.upload_file_path import get_filename_ext


# Create your models here.
def upload_avatar_path(instance, filename):
    name, ext = get_filename_ext(filename)
    random_number = random.randint(1111111, 9999999)
    final_name = f"{random_number}-user-avatar-abdimt{ext}"
    return f"accounts/avatars/{final_name}"


class User(AbstractUser):
    """
    Customize user model.
    """

    bio = models.TextField(default='بیوگرافی خودرا ویرایش کنید', verbose_name='بیوگرافی')
    avatar = models.ImageField(
        upload_to=upload_avatar_path,
        default='accounts/avatars/default.jpg',
        validators=[validate_avatar],
        verbose_name='تصویر پروفایل'
    )
    is_employee = models.BooleanField(default=False, verbose_name='کارمند')
    is_customer = models.BooleanField(default=False, verbose_name='کارفرما')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_supporter = models.BooleanField(default=False, verbose_name='پشتیبان')

    def __str__(self):
        return self.get_full_name()


class PhoneOtp(models.Model):
    """
    The otp codes main model.
    """

    phone = models.CharField(max_length=13)
    code = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'کد تائید'
        verbose_name_plural = 'کد تائید ها'

    def __str__(self):
        return f"{self.phone}"


class IPAddress(models.Model):
    """
    The main IP address model,
    save user information and save current url.
    :model: `accounts.User`
    """

    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="آدرس آیپی")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کاربر")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="ادرس صفحه")
    time = models.DateTimeField(auto_now_add=True, verbose_name="زمان")
    user_agent = models.CharField(max_length=255, verbose_name="اطلاعات سیستم")

    class Meta:
        verbose_name = 'آیپی'
        verbose_name_plural = "آیپی ها"
        ordering = ('-id',)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.ip}"
