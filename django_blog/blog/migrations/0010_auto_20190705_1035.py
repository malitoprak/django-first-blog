# Generated by Django 2.2.2 on 2019-07-05 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190705_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default='default/logo.png', help_text='Kapak Fotoğrafı Yükleyiniz.', null=True, upload_to='blog', verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='kategoriler',
            field=models.ManyToManyField(blank=True, related_name='blog', to='blog.Kategori'),
        ),
    ]
