from django.db import models
from django.shortcuts import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify, safe
from uuid import uuid4
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import os


def upload_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = "%s.%s" % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('blog', unique_id, new_name)


class Kategori(models.Model):
    isim = models.CharField(max_length=10, verbose_name='Kategori İsim')

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.isim


class Blog(models.Model):
    YAYIN_TASLAK = (('all', 'Tümünü seç'), ('yayin', 'YAYIN'), ('taslak', 'TASLAK'))
    user = models.ForeignKey(User, default=1, null=True, verbose_name='User',
                             on_delete=True,
                             related_name='blog')  ##related_name parametresiyle kullanmakta fayda var aslında. user.blog_set yerine user.blog şeklinde erişilebilir bu sayede
    yayin_taslak = models.CharField(choices=YAYIN_TASLAK, max_length=6, null=True, blank=False)

    title = models.CharField(max_length=100, blank=False, null=True, verbose_name='Başlık Giriniz',
                             help_text='Başlık Bilgisi Burada girilir.')
    icerik = RichTextField(null=True, blank=False, max_length=5000, verbose_name='İçerik')
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    image = models.ImageField(verbose_name='Resim', null=True, help_text='Kapak Fotoğrafı Yükleyiniz.', blank=True,
                              default='default/logo.png', upload_to=upload_to)
    # image = models.ImageField(verbose_name='Resim', null=True, help_text='Kapak Fotoğrafı Yükleyiniz.', blank=True, default='default/logo.png', upload_to='blog')
    unique_id = models.CharField(max_length=100, editable=False, null=True)
    slug = models.SlugField(null=True, unique=True, editable=False)

    kategoriler = models.ManyToManyField(to=Kategori, related_name='blog', blank=True)

    class Meta:
        verbose_name_plural = 'Gönderiler'
        ordering = ['-id']

    def __str__(self):
        return "%s %s" % (self.title, self.user)

    @classmethod
    def get_taslak_or_yayin(cls, taslak_yayin):
        return cls.objects.filter(yayin_taslak=taslak_yayin)

    def get_yayin_taslak_html(self):
        if self.yayin_taslak == 'taslak':
            return safe('<small class="label label-{0}">{1}</small>'.format('danger', self.get_yayin_taslak_display()))
        return safe('<small class="label label-{0}">{1}</small>'.format('primary', self.get_yayin_taslak_display()))

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/default/logo.png'

    def get_unique_slug(self):
        slug = slugify(unidecode(self.title))
        new_slug = slug
        sayi = 0
        while Blog.objects.filter(slug=new_slug).exists():
            sayi = sayi + 1
            new_slug = "%s-%s" % (slug, sayi)
        slug = new_slug
        return slug

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_slug()
        else:
            blog = Blog.objects.get(slug=self.slug)
            if blog.title != self.title:
                self.slug = self.get_unique_slug()

        super(Blog, self).save(*args, **kwargs)

    def get_blog_comment(self):
        return self.comment.all().order_by('-id')  ## releated name verdiğimiz için _set demeye gerek yok
        # return self.comment_set.all()

    def get_added_favorite_user(self):
        return self.favorite_blog.values_list('user__username', flat=True)

    def get_comment_count(self):
        yorum_sayisi = self.comment.count()
        if yorum_sayisi > 0 :
            return yorum_sayisi
        return "Henüz Yorum Yok"

    def get_favorite_count(self):
        favori_sayisi = self.favorite_blog.count()
        return favori_sayisi


class Comment(models.Model):
    blog = models.ForeignKey(Blog, null=True, on_delete=True, related_name='comment')
    # isim = models.CharField(blank=True, null=True, verbose_name='İsim', max_length=50)
    # soyisim = models.CharField(blank=True, null=True, verbose_name='Soyisim', max_length=50)
    # email = models.EmailField(blank=False, null=True, verbose_name='Email', help_text='Bu alan zorunludur.')
    # icerik = RichTextField(null=True, blank=False, verbose_name='Yorum', help_text='Fikrinizi yazınız', max_length=1000)
    icerik = models.TextField(verbose_name='Yorum', max_length=1000, blank=False, null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, null=True, default=1, related_name='comment', on_delete=True)

    class Meta:
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return "%s %s" % (self.user, self.blog)

    def get_screen_name(self):
        if self.user.first_name:
            return "%s" % (self.user.get_full_name())
        else:
            return self.user.username


class FavoriteBlog(models.Model):
    blog = models.ForeignKey(Blog, null=True, on_delete=True, related_name='favorite_blog')
    user = models.ForeignKey(User, null=True, default=1, related_name='favorite_blog', on_delete=True)

    def __str__(self):
        return "%s %s" % (self.user, self.blog)

    class Meta:
        verbose_name_plural = "Favorilere eklenen gönderiler"
