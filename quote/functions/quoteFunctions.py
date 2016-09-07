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

    def quoteSearch(self, idcategory, keywords):

        keywords = keywords.split(' ')

        keywords_array=[]
        for keyword in keywords:
            keyword = keyword.strip()
            if(keyword):
                keywords_array.append(keyword)

        quotes = Quote.objects.all()
        if(idcategory != -1):
            quotes = quotes.filter(category__id=idcategory)

        resultIds = {}
        for keyword in keywords:
            quotes2 = quotes.filter(quote__contains=keyword)
            for quote in quotes2:
                if (quote.id in resultIds):
                    resultIds[quote.id] +=1
                else:
                    resultIds[quote.id] = 1

        resultIds = sorted(resultIds, key=resultIds.get)
        resultIds.reverse()

        quotes = Quote.objects.filter(id__in = resultIds)

        quotes_sorted = list()
        for id in resultIds:
            quotes_sorted.append(quotes.get(id=id))

        quotes = quotes_sorted

        return quotes
