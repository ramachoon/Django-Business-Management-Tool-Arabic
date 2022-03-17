# Generated by Django 3.2.5 on 2022-03-17 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_alter_project_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('saturday', 'شنبه'), ('sunday', 'یک شنبه'), ('monday', 'دو شنبه'), ('tuesday', 'سه شنبه'), ('wednesday', 'چهار شنبه'), ('thursday', 'پنجشنبه'), ('friday', 'جمعه')], max_length=20, verbose_name='روز')),
                ('date', django_jalali.db.models.jDateField(verbose_name='تاریخ')),
                ('start_time', models.TimeField(default=django.utils.timezone.now, verbose_name='ساعت شروع کار')),
                ('end_time', models.TimeField(default=django.utils.timezone.now, verbose_name='ساعت پایان کار')),
                ('accessibility', models.CharField(blank=True, choices=[('private', 'خصوصی'), ('public', 'عمومی'), ('only_customer', 'فقط کارفرما')], max_length=13, null=True, verbose_name='دسترسی')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('employees', models.ManyToManyField(related_name='workdays', to=settings.AUTH_USER_MODEL, verbose_name='کارمندان')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workdays', to='projects.project', verbose_name='پروژه')),
            ],
            options={
                'verbose_name': 'روز کاری',
                'verbose_name_plural': 'روزهای کاری',
            },
        ),
    ]
