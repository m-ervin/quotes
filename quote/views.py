# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import RegistrationForm, QuoteForm
from .functions.userFunctions import UserFunctions
from .functions.quoteFunctions import QuoteFunctions
from .models import Quote, Category, Favorite
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
# Create your views here.

def home(request, idcategory = -1):

    quotes = Quote.objects.all().order_by('-id').select_related()
    if(idcategory != -1):
        quotes = quotes.filter(category__id = idcategory)

    paginator = Paginator(quotes,5) #hány darab legyen oldalanként

    page = request.GET.get('page')
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage: # pl. ha túl nagy az oldalszám
        quotes = paginator.page(paginator.num_pages)

    for quote in quotes:
        if(request.user.is_authenticated):
            favorited = Favorite.objects.filter(user= request.user, quote= quote).exists()
        else:
            favorited = False
        quote.favorited = favorited

    return render(request, 'quote/home.html', {'quotes': quotes})

def logoutUser(request):
    logout(request)
    return redirect('homepage')

def registration(request):
    if (request.user.is_authenticated ):
        return redirect ('homepage')
    form = RegistrationForm()

    registerSuccess = False

    if(request.method == "POST"):
        if 'register' in request.POST:
            form = RegistrationForm(request.POST)
            if(form.is_valid()):
                form_data=name=form.cleaned_data
                registerSuccess = UserFunctions().registerUser(form_data['username'], form_data['email'], form_data['password1'])
                form = RegistrationForm

    return render(request, 'quote/registration.html', {'form': form, 'success': registerSuccess})

def addQuote(request):
    if(not request.user.is_authenticated):
        return redirect('homepage')

    addQuoteSuccess = False
    form = QuoteForm()
    if(request.method == "POST"):
        if 'addQuote' in request.POST:
            form = QuoteForm(request.POST)
            if(form.is_valid()):
                form_data=name=form.cleaned_data
                addQuoteSuccess = QuoteFunctions().addQuote( request.user, form_data['category'], form_data['quote'], form_data['author'])
                form = QuoteForm

    return render(request, 'quote/addQuote.html', {'form': form, 'success': addQuoteSuccess })

def categories(request):
    categories = Category.objects.all().order_by("name")
    return render(request, 'quote/categories.html', {'categories': categories})

def quoteModify(request, idquote):
    quote = Quote.objects.filter(id = idquote).get()
    if (quote.user != request.user):
        return redirect('homepage')

    modifySuccess = False
    form = QuoteForm(initial = model_to_dict(quote))
    if(request.method == "POST"):
        if 'modifyQuote' in request.POST:
            form = QuoteForm(request.POST)
            if(form.is_valid()):
                form_data=name=form.cleaned_data
                modifySuccess = QuoteFunctions().modifyQuote(quote.id, form_data['category'], form_data['quote'], form_data['author'])

    return render(request, 'quote/quoteModify.html', {'form': form, 'success': modifySuccess})

def deleteQuote(request):
    deleteSuccess = False
    next = request.POST.get('next','/')
    if(request.method == "POST"):
        idQuote = request.POST.get('id','')
        deleteSuccess = QuoteFunctions().deleteQuote(request.user, idQuote)
    return redirect(next)

def addToFavorites(request):
    if(not request.user.is_authenticated):
        return redirect('homepage')

    if(request.method == "POST"):
        idquote = request.POST.get('idquote',-1)

    state = QuoteFunctions().addToFavorites(request.user, idquote)
    response = {}
    response['state'] = state

    return JsonResponse(response)
