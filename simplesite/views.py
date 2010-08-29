from django.shortcuts import render_to_response
from django.template import RequestContext

from simplesite.models import Page, Menu, Submenu


def page(request, menu_slug, submenu_slug=None):
    """ This is, basically, a wrapper around the 
        menu RequestContextProcessor, allowing us
        to capture URL's that have not been captured
        elsewhere in the URL space. 
    """
    
    # TODO: FINISH THIS
    context = RequestContext(request)
    return render_to_response('simplesite/page.html', request)

    