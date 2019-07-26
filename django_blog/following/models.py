from django.db import models
from django.contrib.auth.models import User


class Following(models.Model):
    follower = models.ForeignKey(User, null=True, verbose_name='Takip eden kullanıcı', related_name='follower',
                                 on_delete=False)
    followed = models.ForeignKey(User, null=True, verbose_name='Takip edilen kullanıcı', related_name='following',
                                 on_delete=False)

    class Meta:
        verbose_name_plural = 'Takipleşme Sistemi'

    def __str__(self):
        return "Follower {} - Followed {}".format(self.follower.username, self.followed.username)

    @classmethod
    def kullanici_takip_et(cls, follower, followed):
        cls.objects.create(follower=follower, followed=followed)

    @classmethod
    def kullaniciyi_takip_ediyor_mu(cls, follower, followed):
        return cls.objects.filter(follower=follower, followed=followed).exists()

    @classmethod
    def kullanici_takipten_cikar(cls, follower, followed):
        cls.objects.filter(follower=follower, followed=followed).delete()

    @classmethod
    def kullanici_takip_edilenler_ve_takipciler(cls, user):
        data = {'takip_edilenler': 0, 'takipciler': 0}
        takip_edilenler = cls.objects.filter(follower=user).count()
        takipciler = cls.objects.filter(followed=user).count()
        # print(takip_edilenler)
        # print(takipciler)
        data.update({'takip_edilenler': takip_edilenler, 'takipciler': takipciler})
        # print(data)
        return data

    @classmethod
    def get_followers(cls, user):
        return cls.objects.filter(followed=user)

    @classmethod
    def get_followed(cls, user):
        return cls.objects.filter(follower=user)

    @classmethod
    def get_followed_username(cls, user):
        followed = cls.get_followed(user)
        return followed.values_list('followed__username', flat=True)
