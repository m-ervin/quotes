"""quotes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="homepage"),
    url(r'^kijelentkezes/$', views.logoutUser, name="logout"),
    url(r'^regisztracio/$', views.registration, name='registration'),
    url(r'^uj_idezet/$', views.addQuote, name="addQoute"),
    url(r'^kategoriak/$', views.categories, name="categories"),
    url(r'^kategoria/(?P<idcategory>[0-9]+)/.*$', views.home, name="homepage_category"),
    url(r'^idezet_modositas/(?P<idquote>[0-9]+)/.*$', views.quoteModify, name="quoteModify"),
    url(r'^idezet_torles/$', views.deleteQuote, name='deleteQuote'),
    url(r'^kedvencekhez/$', views.addToFavorites, name='addToFavorites'),
    url(r'^kedvencek/$', views.favorites, name='favorites' ),
    url(r'^sajat_idezetek/$', views.myQuotes, name='myQuotes')
]
