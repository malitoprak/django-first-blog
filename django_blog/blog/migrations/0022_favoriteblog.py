# Generated by Django 2.2.2 on 2019-07-18 06:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0021_auto_20190717_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(null=True, on_delete=True, related_name='favorite_blog', to='blog.Blog')),
                ('user', models.ForeignKey(default=1, null=True, on_delete=True, related_name='favorite_blog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
