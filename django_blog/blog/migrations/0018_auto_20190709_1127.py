# Generated by Django 2.2.2 on 2019-07-09 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20190709_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=True, related_name='comment', to='blog.Blog'),
        ),
    ]
