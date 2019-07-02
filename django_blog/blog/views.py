from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, HttpResponseRedirect, reverse
from .models import Blog
from .forms import IletisimForm, BlogForm

# Create your views here.

mesajlar = []


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


def post_list(request):
    # request.GET['deneme'] --> bu kullanımda boş dönerse hata alır
    # gelen_deger = request.GET.get('deneme', None) ## Bu kullanım daha doğru
    gelen_deger = request.GET.get('id', None)
    print(gelen_deger)
    posts = Blog.objects.all()
    if gelen_deger:
        posts = posts.filter(id=gelen_deger)
    context = {'posts': posts}
    return render(request, 'blog/post-list.html', context=context)
    ##return render(request, 'blog/post-list.html', context={'key': selam, 'knk': deneme, 'list': liste})


def post_update(request):
    deneme = "Burada gönderi güncellenecektir."
    return HttpResponse(deneme)


def post_delete(request):
    metin = "Burada gönderi silinecektir"
    return HttpResponse(metin)


def post_create(request):
    form = BlogForm
    if request.method == "POST":
        form = BlogForm(data=request.POST)
        if form.is_valid():
            blog = form.save()
            url = reverse('post-detail', kwargs={'pk': blog.pk})
            return HttpResponseRedirect(url)
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


def post_detail(request, pk):
    # try:
    #     blog = Blog.objects.get(pk=pk)
    # except Blog.DoesNotExist:
    #     # return HttpResponse('Böyle bir sayfa bulunamadı')
    #     raise Http404

    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/post-detail.html', context={'blog': blog})
