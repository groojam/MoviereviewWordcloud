# Generated by Django 3.2.3 on 2021-06-17 10:53

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='mvLocation',
            field=models.FileField(default='settings.MEDIA_ROOT/crawldata/anonymous.jpg', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\chase\\OneDrive\\2021project\\mysite\\media'), upload_to='crawldata'),
        ),
    ]
