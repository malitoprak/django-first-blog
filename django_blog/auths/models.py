from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models.signals import post_save

class UserProfile(models.Model):
    SEX = ((None, 'Cinsiyet Seçiniz'),('diger','DIGER'),('erkek','ERKEK'), ('kadın','KADIN'))
    bio = models.TextField(max_length=1000, verbose_name='Hakkımda', blank=True, null=True)
    sex = models.CharField(choices=SEX, blank=True, null=True, max_length=6, verbose_name='Cinsiyet')
    profile_photo = models.ImageField(null=True, blank=True, verbose_name='Profil Fotoğraf')
    dogum_tarihi = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')

    user = models.OneToOneField(User, null=True, blank=False, verbose_name='User', on_delete=True)

    class Meta:
        verbose_name_plural = 'Kullanıcı Profilleri'

    def get_screen_name(self):
        user = self.user
        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def __str__(self):
        return "%s Profile"%(self.get_screen_name())

    def get_user_profile_url(self):
        url = reverse('user-profile', kwargs={'username': self.user.username})
        return url

    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return "/static/img/default.jpg"

    def get_user_full_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return None

def create_profile(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)
