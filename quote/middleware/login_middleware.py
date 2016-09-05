from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate, login

class LoginMiddleware(MiddlewareMixin):
    # Check if client IP is allowed
    def process_request(self, request):
        if(request.method=="POST"):
            r=request.POST
            if ('loginUser' in r):
                user = authenticate (username = r['username'], password = r['password']);
                if (user is not None):
                    login(request, user)
                else:
                    print ('not logged in')


        return
