from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Following
from django.shortcuts import get_object_or_404, Http404
from django.contrib.auth.models import User
from django.template.loader import render_to_string


def kullanici_takip_et_cikar(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()

    data = {'html': '', 'is_valid': True, 'msg': '<b>Takipten çıkar</b>'}
    follower_username = request.GET.get('follower_username', None)
    followed_username = request.GET.get('followed_username', None)

    follower = get_object_or_404(User, username=follower_username)
    followed = get_object_or_404(User, username=followed_username)

    takip_ediyor_mu = Following.kullaniciyi_takip_ediyor_mu(followed=followed, follower=follower)

    if not takip_ediyor_mu:
        Following.kullanici_takip_et(follower=follower, followed=followed)
    else:
        Following.kullanici_takipten_cikar(follower=follower, followed=followed)
        data.update({'msg': '<b>Takip et</b>'})

    takipci_ve_takip_edilen_sayisi = Following.kullanici_takip_edilenler_ve_takipciler(followed)
    context = {'user': followed, 'takipciler': takipci_ve_takip_edilen_sayisi['takipciler'],
               'takip_edilenler': takipci_ve_takip_edilen_sayisi['takip_edilenler']}
    html = render_to_string('auth/profile/include/following/following_partition.html', context=context, request=request)
    # print(html)
    data.update({'html': html})

    return JsonResponse(data=data)


def followed_or_followers_list(request, follow_type):
    data = {'is_valid': True, 'html': ''}
    username = request.GET.get('username', None)
    if not username:
        raise Http404
    user = get_object_or_404(User, username=username)
    my_followed = Following.get_followed_username(user=request.user)

    if follow_type == 'followed':
        takip_edilenler = Following.get_followed(user=user)
        html = render_to_string('following/profile/include/following_followed_list.html',
                                context={'my_followed': my_followed, 'following': takip_edilenler,
                                         'follow_type': follow_type}, request=request)
        data.update({'html': html})

    elif follow_type == 'followers':
        takipciler = Following.get_followers(user=user)
        html = render_to_string('following/profile/include/following_followed_list.html',
                                context={'my_followed': my_followed, 'following': takipciler,
                                         'follow_type': follow_type}, request=request)
        data.update({'html': html})

    else:
        raise Http404

    return JsonResponse(data=data)
