from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
import re


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True,
                               label='Password', min_length=5)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True,
                                       label='Password confirm', min_length=5)

    # sex = forms.ChoiceField(required=True, choices=UserProfile.SEX)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.add_error('password', 'Parolalar Eşleşmedi')
            self.add_error('password_confirm', 'Parolalar Eşleşmedi')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email sistemde kayıtlı.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı sistemde mevcut')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    password = forms.CharField(max_length=50, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('<b>Hatalı kullanıcı adı veya şifre girdiniz.</b>')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match("[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            if len(users) > 0 and len(users) == 1:
                return users.first().username
        return username


class UserProfileUpdateForm(forms.ModelForm):
    sex = forms.ChoiceField(required=True, choices=UserProfile.SEX)
    profile_photo = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    dogum_tarihi = forms.DateField(widget=forms.DateInput(format="%d.%m.%Y"), required=True, label='Doğum Tarihi', input_formats=("%d.%m.%Y",))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'dogum_tarihi', 'profile_photo', 'bio']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['bio'].widget.attrs['rows'] = 10
        DATEPICKER = {
            'type': 'text',
            'class': 'form-control',
            'id': 'datetimepicker1',
            'autocomplete': 'off'
        }
        self.fields['dogum_tarihi'].widget.attrs.update(DATEPICKER)

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if not email:
            raise forms.ValidationError('Lütfen Email Bilgisi giriniz')
        if User.objects.filter(email=email).exclude(
                username=self.instance.username).exists():  ## kendi mail adresi hariç var mı diye kontrol et
            raise forms.ValidationError('Bu email adresi sistemde mevcut.')

        return email


class UserPasswordChangeForm(forms.Form):
    user = None
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Mevcut Şifre',
                                   required=True, min_length=4)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Yeni şifre',
                                   required=True, min_length=4)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                           label='Yeni şifre doğrulama', required=True, min_length=4)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')

        if new_password != new_password_confirm:
            self.add_error('new_password', 'Yeni şifreler eşleşmedi')
            self.add_error('new_password_confirm', 'Yeni şifreler eşleşmedi')

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Lütfen şifrenizi doğru giriniz.')
        return old_password


class UserPasswordChangeForm2(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(UserPasswordChangeForm2, self).__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
