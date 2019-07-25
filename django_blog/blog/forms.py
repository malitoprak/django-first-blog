from django import forms
from .models import Blog, Comment


banned_email_list = ['ahmet@gmail.com', 'deneme@carpedu.com', 'teoman@carpedu.com']


class IletisimForm(forms.Form):
    isim = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label='İsim',
                           required=False)
    soyisim = forms.CharField(max_length=50, label='Soyisim', required=False)
    email = forms.EmailField(max_length=50, label='Email', required=True)
    email2 = forms.EmailField(max_length=50, label="Email Kontrol", required=True)
    icerik = forms.CharField(max_length=1000, label='İçerik')

    def __init__(self, *args, **kwargs):
        super(IletisimForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['icerik'].widget = forms.Textarea(attrs={'class': 'form-control'})
        # self.fields['icerik'] = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_isim(self):
        isim = self.cleaned_data.get('isim')
        if isim == 'ahmet':
            raise forms.ValidationError('Lütfen Ahmet Dışında Bir Kullanıcı Giriniz.')
        return isim

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email in banned_email_list:
            raise forms.ValidationError('Lütfen banlı mail adresleri dışında bir mail giriniz')
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            self.add_error('email2', 'email adresleri eşleşmedi.')
            self.add_error('email', 'email adresleri eşleşmedi.')
            raise forms.ValidationError('***email adresleri eşleşmedi.')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'icerik', 'yayin_taslak', 'kategoriler']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['icerik'].widget.attrs['rows'] = 10

    def clean_icerik(self):
        icerik = self.cleaned_data.get('icerik')
        if len(icerik) < 250:
            msg = 'Lütfen en az 250 karakter giriniz. Girilen karakter sayısı: %s' % len(icerik)
            raise forms.ValidationError(msg)
        return icerik

class PostSorguForm(forms.Form):
    YAYIN_TASLAK = (('all', 'HEPSİ'), ('yayin', 'YAYIN'), ('taslak', 'TASLAK'))

    search = forms.CharField(required=False, max_length=500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Aranacak kelimeyi giriniz'}))
    taslak_yayin = forms.ChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control'}), choices=Blog.YAYIN_TASLAK, required=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}