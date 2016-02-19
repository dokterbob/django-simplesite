import logging
logger = logging.getLogger('simplesite')

from django.core.urlresolvers import resolve, Resolver404

from simplesite.models import Menu, Submenu
from simplesite.utils import ignore_path
from simplesite.settings import URLCONF


def menu(request):
    """ This function puts into the RequestContext:
        - `menu_current`      The current menu (if any)
        - `submenu_current`   The current submenu (if any)
        - `menu_list`         A list of visible main menu items
        - `submenu_list`      A list of visible submenu items for the current menu
    """

    if ignore_path(request.path_info):
        logger.debug('Ignoring path %s in context procesor according to MIDDLEWARE_IGNORE_PATHS.',
                     request.path_info)
        return {}

    logger.error('TEst')
    menu_list = Menu.objects.filter()

    menu_dict = {
        'menu_list': menu_list.filter(visible=True),
        'menu_current': None,
        'submenu_current': None,
        'page_current': None,
        'submenu_list': None,
    }

    try:
        view, args, kwargs = resolve(request.path_info, urlconf=URLCONF)
        logger.debug('menu url matched: args=%s, kwargs=%s', args, kwargs)

        menu_slug = kwargs.get('menu_slug')

        if menu_slug:
            # TODO: This call right here should be made lazy, but would require
            # a wrapper catching exceptions
            menu_obj = menu_list.get(slug=menu_slug)

            logger.debug('menu=%s', menu_obj)

            # Find the corresponding submenu items
            submenu_list = Submenu.objects.filter(menu__slug=menu_slug)

            menu_dict.update({
                'menu_current': menu_obj,
                'submenu_list': submenu_list.filter(visible=True)
            })

            submenu_slug = kwargs.get('submenu_slug')

            if submenu_slug:
                # TODO: This call right here should be made lazy, but would require
                # a wrapper catching exceptions
                submenu_obj = submenu_list.get(slug=submenu_slug)

                logger.debug('submenu=%s', submenu_obj)

                menu_dict.update({'submenu_current': submenu_obj})

                # TODO: This one should be lazy as well
                if submenu_obj.page:
                    menu_dict.update({'page_current': submenu_obj.page})
            else:
                # TODO: This one should be lazy as well
                if menu_obj.page:
                    menu_dict.update({'page_current': menu_obj.page})

    except Resolver404:
        logger.debug("The URL pattern doesn't match any URL.")

    except Menu.DoesNotExist:
        logger.debug("The menu_slug found in the URL match any menu.")

    except Submenu.DoesNotExist:
        logger.debug("The submenu_slug found doesn't match any submenu.")

    return menu_dict
