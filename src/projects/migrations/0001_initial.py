# Generated by Django 3.2.5 on 2022-03-17 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام پروژه')),
                ('description', models.TextField(verbose_name='توضیحات پروژه')),
                ('accessibility', models.CharField(blank=True, choices=[('private', 'خصوصی'), ('public', 'عمومی'), ('only_customer', 'فقط کارفرما')], max_length=13, null=True, verbose_name='دسترسی')),
                ('start_date', django_jalali.db.models.jDateField(verbose_name='تاریخ شروع')),
                ('end_date', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ پایان')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customers', models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='کارفرمایان')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.department', verbose_name='دپارتمان مربوطه')),
            ],
            options={
                'verbose_name': 'پروژه',
                'verbose_name_plural': 'پروژه ها',
            },
        ),
    ]
