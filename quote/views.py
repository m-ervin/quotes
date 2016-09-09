# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import RegistrationForm, QuoteForm, SearchForm, ProfileModifyForm, pictureUploadForm
from .functions.userFunctions import UserFunctions
from .functions.quoteFunctions import QuoteFunctions
from .models import Quote, Category, Favorite, UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
from django.conf import settings
# Create your views here.

def home(request, idcategory = -1):

    keywords = request.GET.get('key','')

    quotes = QuoteFunctions().quoteSearch(idcategory, keywords)

    paginator = Paginator(quotes, settings.QUOTES_PER_PAGE) #hány darab legyen oldalanként

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

    searchForm = SearchForm()

    return render(request, 'quote/home.html', {'quotes': quotes, 'searchForm': searchForm})

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
                registerSuccess = UserFunctions().registerUser(form_data['username'], form_data['email'], form_data['password1'],
                form_data['firstName'], form_data['lastName'])
                form = RegistrationForm

    return render(request, 'quote/user/registration.html', {'form': form, 'success': registerSuccess})

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
    form = QuoteForm(initial = model_to_dict(quote), quote = quote)
    if(request.method == "POST"):
        if 'modifyQuote' in request.POST:
            form = QuoteForm(request.POST, quote = quote)
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

def favorites(request):

    favorites = Favorite.objects.filter(user=request.user).all()
    quotes=[]
    for favorite in favorites:
        quotes.append(favorite.quote)

    paginator = Paginator(quotes, settings.QUOTES_PER_PAGE) #hány darab legyen oldalanként

    page = request.GET.get('page')
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage: # pl. ha túl nagy az oldalszám
        quotes = paginator.page(paginator.num_pages)

    return render(request, 'quote/favorites.html',{'quotes': quotes})

def myQuotes(request):

    quotes = Quote.objects.filter(user = request.user)

    paginator = Paginator(quotes, settings.QUOTES_PER_PAGE) #hány darab legyen oldalanként

    page = request.GET.get('page')
    quotes = paginator.page(paginator.num_pages)

    return render(request, 'quote/myQuotes.html', {'quotes': quotes})


def myProfile(request):
    try:
        profile = UserProfile.objects.filter(user = request.user).get()
        profile = model_to_dict(profile)
    except:
        profile = {}

    userData = model_to_dict(request.user)
    userData.update(profile)

    form = ProfileModifyForm(initial = userData, user = request.user)

    modifySuccess = False

    if(request.method == "POST"):
        form = ProfileModifyForm(request.POST, user = request.user)
        if (form.is_valid()):
            modifySuccess = UserFunctions().modifyUserProfile( request.user, form.cleaned_data )

    return render(request, 'quote/user/myProfile.html', {'form': form, 'success': modifySuccess})

def profilePicture(request):
    form = pictureUploadForm()
    if(request.method == "POST"):
        uploadSuccess = UserFunctions().uploadProfilePicture( request.user, request.FILES['profilePicture'])
    return render(request, 'quote/user/profilePicture.html', {'form': form})
