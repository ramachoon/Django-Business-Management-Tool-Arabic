from django.db import models
from django.urls import reverse
from accounts.models import User


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام دپارتمان')
    staff_users = models.ManyToManyField(
        User, related_name='departments', blank=True, verbose_name='کاربران ارشد'
    )
    description = models.TextField(verbose_name='توضیحات دپارتمان')
    maker = models.ForeignKey(
        User, related_name='departments_owner', on_delete=models.CASCADE, verbose_name='سازنده'
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')

    class Meta:
        verbose_name = 'دپارتمان'
        verbose_name_plural = 'دپارتمان ها'

    def __str__(self):
        return f"{self.name} | {self.description}"

    def get_name_replace(self):
        return f"{self.name.replace(' ', '-')}"

    def get_absolute_url(self):
        return reverse('managers:department_detail', kwargs={'pk': self.id})
