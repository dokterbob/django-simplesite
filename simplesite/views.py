import logging

from django.http import Http404

from django.shortcuts import render_to_response
from django.template import RequestContext

from simplesite.models import Page, Menu, Submenu


def page(request, menu_slug, submenu_slug=None):
    """ This is, basically, a wrapper around the 
        menu RequestContextProcessor, allowing us
        to capture URL's that have not been captured
        elsewhere in the URL space. 
    """
    
    logging.debug('No other view found, resorting to page view with \
                   menu_slug=%s and submenu_slug=%s.' % (menu_slug, submenu_slug))

    context = RequestContext(request)
    
    menu = context.get('menu_current')
    if not menu or not menu.page:
        raise Http404
    
    return render_to_response('simplesite/page.html', context)

    