from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, HttpResponseRedirect, reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from .models import Blog, FavoriteBlog
from .forms import IletisimForm, BlogForm, PostSorguForm, CommentForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from blog.decorators import is_post
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.

mesajlar = []


def deneme_ajax(request):
    if request.is_ajax():
        return JsonResponse(data={'msg': 'Merhaba Dünyaaaa'})
    return HttpResponseBadRequest()


def deneme_ajax2(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()

    context = {'ogrenci': {'isim_soyisim': 'Mali Toprak', 'ogretmen_isim_soyisim': 'Temel Korkmaz'}}
    html = render_to_string('ogrenci_velisine_mesaj.html', context=context, request=request)
    data={'html':html}
    return JsonResponse(data=data)


def deneme(request):
    if request.is_ajax():
        data = {'msg': 'Merhaba Ajax'}
        return JsonResponse(data=data)
    return render(request, 'deneme.html')


def iletisim(request):
    # print(request.GET.get('email'))
    form = IletisimForm(data=request.GET or None)
    if form.is_valid():
        isim = form.cleaned_data.get('isim')
        soyisim = form.cleaned_data.get('soyisim')
        email = form.cleaned_data.get('email')
        icerik = form.cleaned_data.get('icerik')
        data = {'isim': isim, 'soyisim': soyisim, 'email': email, 'icerik': icerik}
        mesajlar.append(data)
        return render(request, 'iletisim.html', context={'mesajlar': mesajlar, 'form': form})

    # print(form)
    return render(request, 'iletisim.html', context={'form': form})


@login_required(login_url=reverse_lazy('user_login'))
def post_list(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('user_login'))
    posts = Blog.objects.all()  # .order_by('id')
    page = request.GET.get('page', 1)
    form = PostSorguForm(data=request.GET or None)
    if form.is_valid():
        taslak_yayin = form.cleaned_data.get('taslak_yayin')
        search = form.cleaned_data.get('search', None)
        if search:
            posts = posts.filter(
                Q(icerik__icontains=search) | Q(title__icontains=search) | Q(
                    kategoriler__isim__icontains=search)).distinct()
        if taslak_yayin and taslak_yayin != 'all':
            posts = posts.filter(yayin_taslak=taslak_yayin)

    # request.GET['deneme'] --> bu kullanımda boş dönerse hata alır
    # gelen_deger = request.GET.get('deneme', None) ## Bu kullanım daha doğru
    # gelen_deger = request.GET.get('id', None)
    # print(gelen_deger)

    # if gelen_deger:
    #     posts = posts.filter(id=gelen_deger)

    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {'posts': posts, 'form': form}
    return render(request, 'blog/post-list.html', context=context)
    ##return render(request, 'blog/post-list.html', context={'key': selam, 'knk': deneme, 'list': liste})


@login_required()  ##SETTINGS DOSYASINDA LOIN_URL'den ALIR BOŞ BIRAKINCA
def post_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user != blog.user:
        return HttpResponseForbidden()
    form = BlogForm(instance=blog, data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        msg = "Tebrikler <strong> %s </strong> isimli gönderiniz başarıyla güncellendi." % blog.title
        messages.success(request, msg, extra_tags='info')
        return HttpResponseRedirect(blog.get_absolute_url())
    context = {'form': form, 'blog': blog}
    return render(request, 'blog/post-update.html', context=context)


@login_required(login_url=reverse_lazy('user_login'))
def post_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user != blog.user:
        return HttpResponseForbidden()
    blog.delete()
    msg = "<strong> %s </strong> isimli gönderiniz silindi." % blog.title
    messages.success(request, msg, extra_tags='danger')
    return HttpResponseRedirect(reverse('post-list'))


@login_required(login_url=reverse_lazy('user_login'))
def post_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    form = BlogForm
    if request.method == "POST":
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            msg = "Tebrikler <strong> %s </strong> isimli gönderiniz başarıyla oluşturuldu." % blog.title
            messages.success(request, msg, extra_tags='success')
            # url = reverse('post-detail', kwargs={'pk': blog.pk})
            # return HttpResponseRedirect(url)
            return HttpResponseRedirect(blog.get_absolute_url())
    return render(request, 'blog/post-create.html', context={'form': form})


def sanatcilar(request, sayi):
    sanatcilar_sozluk = {
        '1': 'Eminem',
        '2': 'Tupack',
        '3': 'Tarkan',
        '4': 'Aleyna Tilki',
        '5': 'Müslüm Gürses',
        '6': 'Neşet Ertaş',
        '98': 'Teoman',
        '9': 'Demir Demirkan',
        'eminem': 'Without me',
        '2e': 'Deneme'
    }

    sanatci = sanatcilar_sozluk.get(sayi, "Bu id numarasina ait sanatçı bulunamadı.")

    return HttpResponse(sanatci)


@login_required(login_url=reverse_lazy('user_login'))
def post_detail(request, slug):
    # try:
    #     blog = Blog.objects.get(pk=pk)
    # except Blog.DoesNotExist:
    #     # return HttpResponse('Böyle bir sayfa bulunamadı')
    #     raise Http404
    form = CommentForm()
    blog = get_object_or_404(Blog, slug=slug)

    return render(request, 'blog/post-detail.html', context={'blog': blog, 'form': form})


@login_required(login_url=reverse_lazy('user_login'))
@is_post
def add_comment(request, slug):
    # if request.method == 'GET':
    #     return HttpResponseBadRequest()
    blog = get_object_or_404(Blog, slug=slug)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.blog = blog
        new_comment.user = request.user
        new_comment.save()
        messages.success(request, 'Tebrikler yorumunuz başarıyla oluşturuldu.')
        return HttpResponseRedirect((blog.get_absolute_url()))


@login_required(login_url=reverse_lazy('user_login'))
def add_or_remove_favorite(request, slug):
    url = request.GET.get('url', None)
    blog = get_object_or_404(Blog, slug=slug)
    favori_blog = FavoriteBlog.objects.filter(blog=blog, user=request.user)
    if favori_blog.exists():
        favori_blog.delete()
    else:
        FavoriteBlog.objects.create(blog=blog, user=request.user)

    if not url:
        url = reverse('post-list')

    return HttpResponseRedirect(url)
