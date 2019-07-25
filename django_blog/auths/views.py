from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UserProfileUpdateForm, UserPasswordChangeForm, UserPasswordChangeForm2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blog.decorators import anonumous_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from blog.models import Blog
from following.models import Following


# Create your views here.

@anonumous_required
def register(request):
    # if not request.user.is_anonymous:
    #     return HttpResponseRedirect(reverse('post-list'))
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        # sex = form.cleaned_data.get('sex')
        user.set_password(raw_password=password)
        user.save()

        # UserProfile.objects.create(user=user, sex=sex)

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, '<b>Tebrikler Kaydınız Başarıyla Gerçekleşti</b>', extra_tags='success')
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())

    return render(request, 'auth/register.html', context={'form': form})


@anonumous_required
def user_login(request):
    # if not request.user.is_anonymous:
    #     return HttpResponseRedirect(reverse('post-list'))
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                msg = "<b>Merhaba %s Sisteme Hoşgeldiniz</b>" % (username)
                messages.success(request, msg, extra_tags='success')
                return HttpResponseRedirect(reverse('post-list'))

    return render(request, 'auth/login.html', context={'form': form})


@login_required
def user_logout(request):
    username = request.user.username
    logout(request)
    msg = '<b>Tekrar görüşmek üzere %s</b>' % (username)
    messages.success(request, msg, extra_tags='success')
    return HttpResponseRedirect(reverse('user_login'))


@login_required
def user_profile(request, username):
    takip_ediyor_mu = False
    user = get_object_or_404(User, username=username)
    blog_list = Blog.objects.filter(user=user)
    takipci_ve_takip_edilen = Following.kullanici_takip_edilenler_ve_takipciler(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']
    # eger kendi profiline girmisse fonksiyon gereksiz calismasin
    if user != request.user:
        takip_ediyor_mu = Following.kullaniciyi_takip_ediyor_mu(follower=request.user, followed=user)
    return render(request, 'auth/profile/userprofile.html',
                  context={'takip_ediyor_mu': takip_ediyor_mu, 'user': user, 'blog_list': blog_list,
                           'page': 'user-profile', 'takipciler': takipciler, 'takip_edilenler': takip_edilenler})


@login_required
def user_settings(request):
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    dogum_tarihi = request.user.userprofile.dogum_tarihi
    takipci_ve_takip_edilen = Following.kullanici_takip_edilenler_ve_takipciler(request.user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']
    initial = {'sex': sex, 'bio': bio, 'profile_photo': profile_photo, 'dogum_tarihi': dogum_tarihi}
    form = UserProfileUpdateForm(initial=initial, instance=request.user, data=request.POST or None,
                                 files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=True)  ##user modeli eklendi userprofile ayrıca eklenecek
            bio = form.cleaned_data.get('bio', None)
            sex = form.cleaned_data.get('sex', None)
            profile_photo = form.cleaned_data.get('profile_photo', None)
            dogum_tarihi = form.cleaned_data.get('dogum_tarihi')
            user.userprofile.sex = sex
            user.userprofile.profile_photo = profile_photo
            user.userprofile.dogum_tarihi = dogum_tarihi
            user.userprofile.bio = bio
            user.userprofile.save()
            messages.success(request, 'Tebrikler Kullanıcı Bilgileriniz Başarıyla Güncellendi', extra_tags='success')
            return HttpResponseRedirect(reverse('user-profile', kwargs={'username': user.username}))
        else:
            messages.warning(request, 'Lütfen form alanlarını doğru giriniz', extra_tags='danger')

    return render(request, 'auth/profile/settings.html',
                  context={'form': form, 'page': 'settings', 'takipciler': takipciler,
                           'takip_edilenler': takip_edilenler})


@login_required
def user_about(request, username):
    user = get_object_or_404(User, username=username)
    takip_ediyor_mu = False
    takipci_ve_takip_edilen = Following.kullanici_takip_edilenler_ve_takipciler(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']
    if user != request.user:
        takip_ediyor_mu = Following.kullaniciyi_takip_ediyor_mu(follower=request.user, followed=user)
    return render(request, 'auth/profile/about_me.html',
                  context={'user': user, 'page': 'about', 'takip_ediyor_mu': takip_ediyor_mu, 'takipciler': takipciler,
                           'takip_edilenler': takip_edilenler})


@login_required
def user_password_change(request):
    # form = UserPasswordChangeForm(user=request.user, data=request.POST or None)
    # form = PasswordChangeForm(user=request.user, data=request.POST or None)
    form = UserPasswordChangeForm2(user=request.user, data=request.POST or None)

    takipci_ve_takip_edilen = Following.kullanici_takip_edilenler_ve_takipciler(request.user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    if form.is_valid():
        # new_password = form.cleaned_data.get('new_password')
        # request.user.set_password(new_password)
        # request.user.save()
        form.save(commit=True)
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Tebrikler şifreniz başarıyla güncellendi', extra_tags='success')
        return HttpResponseRedirect(reverse('user-profile', kwargs={'username': request.user.username}))
    return render(request, 'auth/profile/password_change.html',
                  context={'form': form, 'page': 'password-change', 'takipciler': takipciler,
                           'takip_edilenler': takip_edilenler})
