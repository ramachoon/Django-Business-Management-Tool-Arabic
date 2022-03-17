from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from departments.models import Department
from django_jalali.db import models as jmodels
from src.extensions.utils import jalali_converter

# Create your models here.

ACCESSIBILITY_CHOICES = (
    ('private', 'خصوصی'),
    ('public', 'عمومی'),
    ('only_customer', 'فقط کارفرما')
)


class Project(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام پروژه')
    description = models.TextField(verbose_name='توضیحات پروژه')
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name='دپارتمان مربوطه', related_name='projects'
    )
    customers = models.ManyToManyField(
        User, related_name='projects', verbose_name='کارفرمایان'
    )
    accessibility = models.CharField(
        max_length=13, choices=ACCESSIBILITY_CHOICES, null=True, blank=True, verbose_name='دسترسی'
    )
    start_date = jmodels.jDateField(verbose_name='تاریخ شروع')
    end_date = jmodels.jDateField(verbose_name='تاریخ پایان', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه ها'

    def __str__(self):
        return f"{self.name} -> {self.department.name}"

    def get_created_jalali(self):
        return jalali_converter(self.created)

    def get_updated_jalali(self):
        return jalali_converter(self.updated)

    def get_name_replace(self):
        return f"{self.name.replace(' ', '-')}"

    # def get_absolute_url(self):
    #     return reverse('projects:detail', kwargs={'pk': self.pk, 'name': self.get_name_replace()})

    def get_progress(self):
        start_date = self.start_date
        end_date = self.end_date
        now_date = timezone.now().date()
        initial_date = end_date - start_date
        final_date = end_date - now_date
        if initial_date != 0 and final_date != 0:
            progress = ((final_date.days - initial_date.days) / initial_date.days) * 100
            if progress < 0:
                progress = -progress

        return {
            'initial_date': initial_date.days,
            'final_date': final_date.days,
            'progress': int(progress)
        }
