# Generated by Django 3.2.3 on 2021-05-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('mvId', models.IntegerField(primary_key=True, serialize=False)),
                ('mvName', models.CharField(max_length=200)),
                ('mvData', models.TextField()),
            ],
        ),
    ]
