# Generated by Django 4.2.7 on 2023-11-02 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeroom', '0004_auto_20220529_1937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kaladetail',
            options={'ordering': ('-id',), 'verbose_name': 'جزئیات کالا', 'verbose_name_plural': 'جزئیات کالا ها'},
        ),
        migrations.AlterModelOptions(
            name='kalahistory',
            options={'ordering': ('-id',), 'verbose_name': 'سابقه کالا', 'verbose_name_plural': 'سابقه کالا ها'},
        ),
    ]
