# Generated by Django 3.2.5 on 2022-03-19 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ('-id',), 'verbose_name': 'دپارتمان', 'verbose_name_plural': 'دپارتمان ها'},
        ),
    ]
