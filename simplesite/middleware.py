import logging

from simplesite.views import page
from django.http import Http404
from django.conf import settings

class SimplesiteFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        
        logging.debug('Normal processing returned a 404, resort to simplesite')
        try:
            return page(request)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            logging.debug('Even simplesite returned a 404 error. Really, you\'re quite fucked up.')
            return response
        except:
            if settings.DEBUG:
                raise
            return response
