from django import forms
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import User

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

    username = forms.CharField(label='Felhasználónév', max_length=30, validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$',
    message='Csak betű, szám és aláhúzásjel')])
    email = forms.CharField(label='Email', max_length=50, validators=[EmailValidator(message='Hibás email cím')] )
    password1 = forms.CharField(label='Jelszó', max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Jelszó újból', max_length=50, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required':'Nem lehet üres mező'.format(
                fieldname=field.label)}
