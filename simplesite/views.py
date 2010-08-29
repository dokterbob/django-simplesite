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
    # 1) Assert the menu context_processor is present
    # 2) Fetch the current menu and submenu from the context
    # 3) See whether there's a corresponding page
    # 4)a If so, continue.
    # 4)b If not: raise 404 or some other error (design decision). 
    context = RequestContext(request)
    return render_to_response('simplesite/page.html', request)

    