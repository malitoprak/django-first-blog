# Generated by Django 2.2.2 on 2019-07-23 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_favoriteblog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriteblog',
            options={'verbose_name_plural': 'Favorilere eklenen gönderiler'},
        ),
    ]