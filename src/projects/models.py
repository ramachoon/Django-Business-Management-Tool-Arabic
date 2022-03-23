import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from departments.models import Department
from django_jalali.db import models as jmodels

from .managers import WorkDayManager
from src.extensions.utils import jalali_converter

# Create your models here.

ACCESSIBILITY_CHOICES = (
    ('private', 'خصوصی'),
    ('public', 'عمومی'),
    ('only_customer', 'فقط کارفرما')
)

DAYS_CHOICES = (
    ('saturday', 'شنبه'),
    ('sunday', 'یک شنبه'),
    ('monday', 'دو شنبه'),
    ('tuesday', 'سه شنبه'),
    ('wednesday', 'چهار شنبه'),
    ('thursday', 'پنجشنبه'),
    ('friday', 'جمعه'),
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
        ordering = ('-id',)

    def __str__(self):
        return f"{self.name} -> {self.department.name}"

    def get_created_jalali(self):
        return jalali_converter(self.created)

    def get_updated_jalali(self):
        return jalali_converter(self.updated)

    def get_name_replace(self):
        return f"{self.name.replace(' ', '-')}"

    def get_absolute_url(self):
        return reverse('managers:project_detail', kwargs={'pk': self.pk})

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

    def get_total_expenses(self):
        total = 0
        for factor in self.invoices.all():
            total += factor.get_total_invoice_price()

        return total

    def get_total_expenses_paid(self):
        total = 0
        for factor in self.invoices.filter(is_paid=True).all():
            total += factor.get_total_invoice_price()

        return total


class WorkDay(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='پروژه', related_name='workdays'
    )
    day = models.CharField(max_length=20, choices=DAYS_CHOICES, verbose_name='روز')
    date = jmodels.jDateField(verbose_name='تاریخ')
    start_time = models.TimeField(default=timezone.now, verbose_name='ساعت شروع کار')
    end_time = models.TimeField(default=timezone.now, verbose_name='ساعت پایان کار')
    accessibility = models.CharField(
        max_length=13, choices=ACCESSIBILITY_CHOICES, null=True, blank=True, verbose_name='دسترسی'
    )
    employees = models.ManyToManyField(User, related_name='workdays', verbose_name='کارمندان')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'روز کاری'
        verbose_name_plural = 'روزهای کاری'
        ordering = ('-date',)

    objects = WorkDayManager()

    def __str__(self):
        return f"{self.date.year}/{self.date.month}/{self.date.day} | {self.get_day_display()}"

    def get_name_replace(self):
        return f"{self.date.year}-{self.date.month}-{self.date.day}-{self.day}"

    def get_created_jalali(self):
        return jalali_converter(self.created)

    def get_updated_jalali(self):
        return jalali_converter(self.updated)

    def get_absolute_url(self):
        return reverse('managers:workday_detail', kwargs={'pk': self.pk})


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_description = models.CharField(max_length=100, verbose_name='توضیح کوتاه')
    date = jmodels.jDateField(verbose_name='تاریخ')
    project = models.ForeignKey(
        Project, related_name='invoices', on_delete=models.CASCADE, verbose_name='پروژه'
    )
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده / نشده')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'صورتحساب'
        verbose_name_plural = 'صورتحساب ها'
        ordering = ('-id',)

    def get_total_invoice_price(self):
        total = 0
        for invoice_detail in self.invoice_details.all():
            total += invoice_detail.get_total_price()

        return total

    def __str__(self):
        return f"{self.short_description} | جمع فاکتور: {self.get_total_invoice_price()} تومان"


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name='invoice_details', on_delete=models.CASCADE, verbose_name='صورتحساب'
    )
    name = models.CharField(max_length=75, verbose_name='نام')
    quantity = models.BigIntegerField(default=1, verbose_name='مقدار')
    amount = models.BigIntegerField(verbose_name='قیمت')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'جزئیات صورتحساب'
        verbose_name_plural = 'جزئیات صورتحساب ها'

    def get_total_price(self):
        return self.quantity * self.amount

    def __str__(self):
        return f"جمع: {self.get_total_price()} تومان"
