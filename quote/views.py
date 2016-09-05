from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import RegistrationForm
from .functions.userFunctions import UserFunctions
# Create your views here.

def home(request):
    return render(request, 'quote/home.html')

def logoutUser(request):
    logout(request)
    return redirect('homepage')

def registration(request):
    form = RegistrationForm()

    if(request.method == "POST"):
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            form_data=name=form.cleaned_data
            UserFunctions.registerUser(form_data['username'], form_data['email'], form_data['password1'])
            form = RegistrationForm

    return render(request, 'quote/registration.html', {'form': form})
