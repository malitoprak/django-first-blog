from django.contrib import admin
from .models import Blog, Kategori, Comment, FavoriteBlog


# Register your models here.


admin.site.register(Blog)
admin.site.register(Kategori)
admin.site.register(Comment)
admin.site.register(FavoriteBlog)