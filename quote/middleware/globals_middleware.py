from django.utils.deprecation import MiddlewareMixin
from ..models import Category

class GlobalsMiddleware(MiddlewareMixin):
    # Check if client IP is allowed
    def process_request(self, request):

        categories = Category.objects.all()
        request.categories = categories

        request.showSideMenuUrls = ['homepage', 'homepage_category']

        return
