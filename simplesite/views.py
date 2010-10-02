import logging

from django.http import Http404

from django.shortcuts import render_to_response
from django.template import RequestContext

from simplesite.models import Page, Menu, Submenu

logger = logging.getLogger('simplesite')

def page(request, menu_slug=None, submenu_slug=None):
    """ This is, basically, a wrapper around the 
        menu RequestContextProcessor, allowing us
        to capture URL's that have not been captured
        elsewhere in the URL space. 
        
        Templates are looked for in several directories,
        making it easy to customize the looks of a particular
        part of the site:
        
        simplesite/page.html
        simplesite/<menu_current.slug>/page.html
        simplesite/<menu_current.slug>/<submenu_current.slug>/page.html
        
        In these menu, all the variables from the context_processor are
        fully available, as in other pages within the site.
    """
    
    context = RequestContext(request)

    page = context.get('page_current')
    if not (page and page.publish):
        raise Http404
        
    submenu = context.get('submenu_current')
    menu = context.get('menu_current')

    template_names = []
    if submenu:
        template_names.append('simplesite/%s/%s/page.html' % \
                                (menu.slug, submenu.slug))
    if menu:
        template_names.append('simplesite/%s/page.html' % menu.slug)
    
    template_names.append('simplesite/page.html')
    
    logger.debug('Searching for templates in %s' % template_names)
    
    return render_to_response(template_names, context)

    