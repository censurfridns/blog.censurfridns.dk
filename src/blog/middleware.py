from django.conf import settings
from django.utils import translation

class SetLanguageFromDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ### set language from domain
        if request.META['HTTP_HOST'] in settings.LANGUAGE_BY_DOMAIN:
            user_language = settings.LANGUAGE_BY_DOMAIN[request.META['HTTP_HOST']]
            translation.activate(user_language)
            response = self.get_response(request)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
            return response
        return self.get_response(request)
