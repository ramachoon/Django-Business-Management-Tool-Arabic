import random

import qrcode
from django.db import models
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.urls import reverse
from django_jalali.db import models as jmodels

from extensions.utils import generate_kala_id


# Create your models here.


class Kala(models.Model):
    FILTER_CHOICES = (
        ('0', 'انبار مصرفی'),
        ('1', 'انبار ابزار'),
    )

    id = models.CharField(
        max_length=255, default=generate_kala_id, primary_key=True, editable=False, unique=True
    )
    name = models.CharField(max_length=100, verbose_name='نام کالا')
    qr_image = models.ImageField(upload_to='kala/qr/', blank=True, null=True, verbose_name='QRCode')
    description = models.TextField(verbose_name='توضیحات')
    filter = models.CharField(max_length=10, choices=FILTER_CHOICES, verbose_name='انبار')

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا ها'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('managers:kala_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.qr_image:
            qr_image = qrcode.make(reverse('managers:kala_detail', kwargs={'pk': self.pk}))
            qr_offset = Image.new('RGB', (350, 350), 'white')
            draw_img = ImageDraw.Draw(qr_offset)
            qr_offset.paste(qr_image)
            file_name = f'AB-QR-{random.randint(10000000, 99999999)}.png'
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            self.qr_image.save(file_name, File(stream), save=False)
            qr_offset.close()
        super().save(*args, **kwargs)


class KalaDetail(models.Model):
    kala = models.ForeignKey(
        Kala, related_name='kala_details', on_delete=models.CASCADE, verbose_name='کالا'
    )
    name = models.CharField(max_length=100, verbose_name='نام')
    quantity = models.CharField(max_length=50, blank=True, null=True, verbose_name='واحد')
    price = models.CharField(max_length=50, blank=True, null=True, verbose_name='قیمت')
    total = models.CharField(max_length=50, blank=True, null=True, verbose_name='جمع قیمت')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'جزئیات کالا'
        verbose_name_plural = 'جزئیات کالا ها'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.name}"


class KalaHistory(models.Model):
    kala = models.ForeignKey(
        Kala, related_name='kala_histories', on_delete=models.CASCADE, verbose_name='کالا'
    )
    date = jmodels.jDateField(verbose_name='تاریخ')
    short_description = models.CharField(max_length=150, verbose_name='توضیح سابقه')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'سابقه کالا'
        verbose_name_plural = 'سابقه کالا ها'

    def __str__(self):
        return f"{self.short_description}"
