# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import RegistrationForm, AddQuoteForm
from .functions.userFunctions import UserFunctions
from .functions.quoteFunctions import QuoteFunctions
from .models import Quote, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def home(request):
    quotes=Quote.objects.all()
    paginator=Paginator(quotes,5) #hány darab legyen oldalanként

    page=request.GET.get('page')
    try:
        quotes=paginator.page(page)
    except PageNotAnInteger:
        quotes=paginator.page(1)
    except EmptyPage: # pl. ha túl nagy az oldalszám
        quotes=paginator.page(paginator.num_pages)

    return render(request, 'quote/home.html', {'quotes': quotes})

def logoutUser(request):
    logout(request)
    return redirect('homepage')

def registration(request):
    form = RegistrationForm()

    print(request.user);

    if(request.method == "POST"):
        if 'register' in request.POST:
            form = RegistrationForm(request.POST)
            if(form.is_valid()):
                form_data=name=form.cleaned_data
                UserFunctions().registerUser(form_data['username'], form_data['email'], form_data['password1'])
                form = RegistrationForm

    return render(request, 'quote/registration.html', {'form': form})

def addQuote(request):
    if(not request.user.is_authenticated):
        return redirect('homepage')

    form = AddQuoteForm()
    if(request.method == "POST"):
        if 'addQuote' in request.POST:
            form = AddQuoteForm(request.POST)
            if(form.is_valid()):
                form_data=name=form.cleaned_data
                addQuoteSuccess = QuoteFunctions().addQuote( request.user, form_data['category'], form_data['quote'], form_data['author'])
                form = AddQuoteForm

    return render(request, 'quote/addQuote.html', {'form': form, 'success': addQuoteSuccess })
