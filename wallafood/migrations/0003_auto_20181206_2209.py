# Generated by Django 2.1.3 on 2018-12-06 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallafood', '0002_auto_20181205_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='vendor',
            field=models.CharField(max_length=200),
        ),
    ]
