# Generated by Django 2.2.2 on 2019-07-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_auto_20190711_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[(None, 'Cinsiyet Seçiniz'), ('diger', 'DIGER'), ('erkek', 'ERKEK'), ('kadın', 'KADIN')], max_length=6, null=True, verbose_name='Cinsiyet'),
        ),
    ]
