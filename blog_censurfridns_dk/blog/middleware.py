from django.conf import settings

class SetLanguageFromDomainMiddleware(object):
    def process_request(self, request):
        if 'LANGUAGE_SESSION_KEY' not in request.session:
            ### set language from domain
            if request.META['HTTP_HOST'] in settings.LANGUAGE_BY_DOMAIN:
                user_language = settings.LANGUAGE_BY_DOMAIN[request.META['HTTP_HOST']]
                translation.activate(user_language)
                request.session[LANGUAGE_SESSION_KEY] = user_language

