# Generated by Django 2.2.2 on 2019-07-17 08:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_blog_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Gönderiler'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=True, related_name='blog', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
