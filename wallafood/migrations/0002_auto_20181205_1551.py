# Generated by Django 2.1.3 on 2018-12-05 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallafood', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='photo_url',
            field=models.CharField(default='', max_length=300),
        ),
    ]