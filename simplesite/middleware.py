import logging
logger = logging.getLogger('simplesite')

from django.http import Http404
from django.conf import settings

from simplesite.views import page
from simplesite.utils import ignore_path


class SimplesiteFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.

        if ignore_path(request.path_info):
            logger.debug('Ignoring path %s in middleware according to MIDDLEWARE_IGNORE_PATHS.',
                         request.path_info)

            return response

        logger.debug('Normal processing returned a 404, resort to simplesite')
        try:
            return page(request)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            logger.debug('Even simplesite returned a 404.')
            return response
        except:
            if settings.DEBUG:
                raise
            else:
                # Fail silently, but do logging
                logger.exception('Something went wrong trying to serve a page')
            
            return response
