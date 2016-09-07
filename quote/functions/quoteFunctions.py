# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from ..models import Category, Quote, Favorite
from django.shortcuts import get_object_or_404

class QuoteFunctions(object):

    def addQuote(self, user, category, quote, author):
        if not author:
            author = 'Ismeretlen'
        q = Quote(category = category, quote = quote, author = author, user = user)
        q.save()
        return True

    def modifyQuote(self, idQuote, category, text, author):
        if not author:
            author = 'Ismeretlen'
        quote = Quote.objects.filter(id=idQuote).get()
        quote.category = category
        quote.quote = text
        quote.author = author
        quote.save()
        return True

    def deleteQuote(self, user, idQuote):
        quote = get_object_or_404(Quote, id = idQuote)
        if( quote.user != user ):
            return False

        quote.delete()
        return True

    def addToFavorites(self, user, idquote):
        quote = get_object_or_404(Quote, id = idquote)
        obj, created = Favorite.objects.get_or_create(user=user, quote=quote)
        if (created == False):
            obj.delete()
            favorited = False
        else:
            favorited = True

        return favorited
