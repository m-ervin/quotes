# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import EmailValidator, RegexValidator, MaxLengthValidator
from django.contrib.auth.models import User
from .models import Category, Quote

class LoginForm(forms.Form):
    username = forms.CharField(label='Felhasználónév', max_length=30)
    password = forms.CharField(label='Jelszó', max_length=50, widget=forms.PasswordInput())

class RegistrationForm(forms.Form):

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            self.add_error("password2", "A két jelszó nem azonos")

        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            self.add_error('email','Ez az email cím már használatban van')

        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            self.add_error('username','Ilyen felhasználónevű felhasználó már létezik')

        return self.cleaned_data

    username = forms.CharField(label='Felhasználónév', max_length=30, validators=[RegexValidator(regex='^[a-zA-Z0-9_\.]+$',
    message='Csak betű, szám, aláhúzásjel és pont')])
    lastName = forms.CharField(label = 'Vezetéknév', max_length=30)
    firstName = forms.CharField(label = 'Név', max_length=30)
    email = forms.CharField(label='Email', max_length=50, validators=[EmailValidator(message='Hibás email cím')] )
    password1 = forms.CharField(label='Jelszó', max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Jelszó újból', max_length=50, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required':'Nem lehet üres mező'.format(
                fieldname = field.label)}


class ProfileModifyForm(RegistrationForm):

    def clean(self):
        if User.objects.filter(email = self.cleaned_data.get('email')).exclude(email = self.user.email).exists():
            self.add_error('email','Ez az email cím már használatban van')

        if User.objects.filter(username=self.cleaned_data.get('username')).exclude(username = self.user.username).exists():
            self.add_error('username','Ilyen felhasználónevű felhasználó már létezik')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')

        for field in self.fields.values():
            field.error_messages = {'required':'Nem lehet üres mező'.format(
                fieldname = field.label)}


class QuoteForm(forms.Form):

    def clean(self):
        if Quote.objects.filter(quote=self.cleaned_data.get('quote')).exclude(id = self.quote.id).exists():
            self.add_error('quote','Ez az idézet már szerepel az adatbázisban')

        return self.cleaned_data


    categories=Category.objects.all()
    category = forms.ModelChoiceField(label = 'Kategória', queryset = categories, initial = 0)
    quote = forms.CharField(label = 'Idézet',  help_text = '*', validators = [MaxLengthValidator(500, message = 'max 500 karakter')], widget = forms.Textarea())
    author = forms.CharField(label = 'Szerző', max_length = 50, required = False, widget=forms.TextInput(attrs={'placeholder': 'Ismeretlen'}))


    def __init__(self, *args, **kwargs):
        self.quote = kwargs.pop('quote', None)
        super(QuoteForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required':'Nem lehet üres mező'.format(
                fieldname = field.label)}

class SearchForm(forms.Form):

    key = forms.CharField(label = 'Keresés')


class pictureUploadForm(forms.Form):

    profilePicture = forms.FileField()
