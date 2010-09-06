import logging

from django.http import Http404

from django.shortcuts import render_to_response
from django.template import RequestContext

from simplesite.models import Page, Menu, Submenu


def page(request, menu_slug=None, submenu_slug=None):
    """ This is, basically, a wrapper around the 
        menu RequestContextProcessor, allowing us
        to capture URL's that have not been captured
        elsewhere in the URL space. 
    """
    
    context = RequestContext(request)

    page = context.get('page_current')
    if not (page and page.publish):
        raise Http404
    
    return render_to_response('simplesite/page.html', context)

    