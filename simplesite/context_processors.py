from django.core.urlresolvers import resolve

from simplesite.models import Menu, Submenu

from simplesite.urls import urlpatterns

def menu(request):
    """ This function puts into the RequestContext:
        - `menu_current`      The current menu (if any)
        - `submenu_current`   The current submenu (if any)
        - `menu_list`         A list of visible main menu items
        - `submenu_list`      A list of visible submenu items for the current menu
    """
    
    # Only select visible menu items
    menu_visible = Menu.objects.filter(visible=True)

    menu_dict = {'menu_list': menu_visible }
                 
    try:    
        # Use the urlspace configuration from urls.py to
        # resolve menu_slug and submenu_slug parameters
        view, args, kwargs = resolve(path, urlconf=urlpatterns)

        menu_slug = getattr(kwargs, 'menu_slug', None)
        if menu_slug:
            menu_obj = menu_visible.get(slug=menu_slug)
            
            # Find the corresponding submenu items
            submenu_visible = Submenu.objects.filter(visible=True,
                                                     menu=menu_obj)
            
            menu_dict.update({'menu_current': menu_obj,
                              'submenu_list': submenu_visible})
    
            submenu_slug = getattr(kwargs, 'submenu_slug', None)
            if submenu_slug:
                submenu_obj = submenu_visible.get(slug=submenu_slug)
                
                menu_dict.update({'submenu_current': submenu_obj})
                
    except (Resolver404, Menu.DoesNotExist, Submenu.DoesNotExist):
        # Resolver404: the URL pattern doesn't match any URL
        # Menu.DoesNotExist: the menu_slug found in the URL match any menu
        # Submenu.DoesNotExist: the submenu_slug found doesn't match any submenu
        pass
    
    return menu_dict
