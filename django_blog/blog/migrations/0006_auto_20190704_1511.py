# Generated by Django 2.2.2 on 2019-07-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_kategoriler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='kategoriler',
            field=models.ManyToManyField(null=True, related_name='blog', to='blog.Kategori'),
        ),
    ]