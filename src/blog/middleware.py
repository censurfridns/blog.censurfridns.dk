from django.conf import settings
from django.utils import translation

class SetLanguageFromDomainMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        ### set language from domain
        if request.META['HTTP_HOST'] in settings.LANGUAGE_BY_DOMAIN:
            user_language = settings.LANGUAGE_BY_DOMAIN[request.META['HTTP_HOST']]
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language

