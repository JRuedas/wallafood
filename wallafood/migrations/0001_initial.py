# Generated by Django 2.1.3 on 2018-11-12 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_movie', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('vendor', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('amout_available', models.IntegerField()),
                ('allergens', models.CharField(max_length=200)),
                ('vote_average', models.DecimalField(decimal_places=2, max_digits=3)),
                ('status', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
