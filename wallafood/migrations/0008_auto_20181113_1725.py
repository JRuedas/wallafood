# Generated by Django 2.1.3 on 2018-11-13 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallafood', '0007_auto_20181113_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='id_advert',
            field=models.IntegerField(default=0),
        ),
    ]
