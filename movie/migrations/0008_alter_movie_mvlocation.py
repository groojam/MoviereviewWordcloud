# Generated by Django 3.2.3 on 2021-06-17 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_auto_20210618_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='mvLocation',
            field=models.TextField(null=True),
        ),
    ]
