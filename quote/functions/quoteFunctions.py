# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from ..models import Category, Quote

class QuoteFunctions(object):

    def addQuote(self, user, category, quote, author):
        if not author:
            author = 'Ismeretlen'
        q = Quote(category = category, quote = quote, author = author, user = user)
        q.save()
        return True

        # subject = 'Aktivációs email'
        # message = 'aktivacio'
        # toEmail = 'ervinmartatic@gmail.com'
        # send_mail(subject, message, 'quotes@gmail.com',[toEmail], fail_silently = False)
