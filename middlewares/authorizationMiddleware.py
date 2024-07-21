from response import Response
from user.models import User
from user.urls import whitelist as user_whitelist
from user.views.user.utils import get_token_data

from django.utils import timezone

whitelist = user_whitelist

class AuthorizationMiddleware:
    whitelist = whitelist
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != 'GET' and request.method != "OPTIONS":
            if request.path_info not in whitelist:
                try:
                    auth = request.META.get("HTTP_AUTHORIZATION", None)
                    if auth is None:
                        return Response.token_error()
                    auth = auth.split(" ")
                except AttributeError:
                    return Response.token_error()
                if auth[0].lower() == "token" and len(auth) == 2:
                    data = get_token_data(auth[1])
                    if data["token"] == "" or data["username"] == "":
                        return Response.token_error()
                    try:
                        user = User.objects.get(username=data["username"])
                        if user.token != data["token"] or (timezone.now() - user.token_expiration_time).total_seconds() > 0:
                            return Response.token_error()
                    except:
                        return Response.token_error()
                else:
                    return Response.token_error()
        
        response = self.get_response(request)
        return response