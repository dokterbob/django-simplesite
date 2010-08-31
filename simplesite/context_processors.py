import logging

from django.core.urlresolvers import resolve, Resolver404

from simplesite.models import Menu, Submenu


def menu(request):
    """ This function puts into the RequestContext:
        - `menu_current`      The current menu (if any)
        - `submenu_current`   The current submenu (if any)
        - `menu_list`         A list of visible main menu items
        - `submenu_list`      A list of visible submenu items for the current menu
    """
    
    # Only select visible menu items
    menu_visible = Menu.objects.filter(visible=True)
    logging.debug('Adding menu items to context: %s', menu_visible)

    menu_dict = {'menu_list': menu_visible }
                 
    try:    
        view, args, kwargs = resolve(request.path, urlconf='simplesite.urls')
        logging.debug('menu url matched: args=%s, kwargs=%s', args, kwargs)

        menu_slug = kwargs.get('menu_slug')
        if menu_slug:
            menu_obj = menu_visible.get(slug=menu_slug)
            logging.debug('menu=%s', menu_obj)

            
            # Find the corresponding submenu items
            submenu_visible = Submenu.objects.filter(visible=True,
                                                     menu=menu_obj)
            
            menu_dict.update({'menu_current': menu_obj,
                              'submenu_list': submenu_visible})
                              
            submenu_slug = kwargs.get('submenu_slug')
            if submenu_slug:
                submenu_obj = submenu_visible.get(slug=submenu_slug)
                logging.debug('submenu=%s', submenu_obj)
                
                menu_dict.update({'submenu_current': submenu_obj})
                
    except (Resolver404, Menu.DoesNotExist, Submenu.DoesNotExist) as e:
        # Resolver404: the URL pattern doesn't match any URL
        # Menu.DoesNotExist: the menu_slug found in the URL match any menu
        # Submenu.DoesNotExist: the submenu_slug found doesn't match any submenu
        
        logging.debug('Current menu item not identified, error: %s' % e)
    
    return menu_dict
