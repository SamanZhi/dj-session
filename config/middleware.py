from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .session import SessionStore


def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))

class MySessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)

        return self.process_response(request, response)

    def process_request(self, request):
        session_key = request.COOKIES.get("sessionid")
        request.session = SessionStore(session_key)
        
    def process_response(self, request, response):
        if request.session.modified:
            request.session.save()

        response.set_cookie("sessionid", request.session.session_key)

        return response