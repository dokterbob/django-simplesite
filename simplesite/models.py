from django.db import models

from django.utils.translation import ugettext_lazy as _

from metadata.models import DateAbstractBase, \
                            TitleAbstractBase, \
                            SlugAbstractBase 

class Page(TitleAbstractBase, DateAbstractBase):
    """ Class representing a page with title and contents """
    
    publish = models.BooleanField(verbose_name=_('publish'),
                                  default=True, db_index=True)
    content = models.TextField(verbose_name=_('content'))
    
    class Meta:
        ordering = ['title',]
        verbose_name = _('page')
        verbose_name_plural = _('pages')


def get_next_ordering(cls):
    ordering = cls.objects.aggregate(models.Max('ordering'))['ordering__max']
    if ordering:
        return ordering+10
    else:
        return 10

    
class MenuBase(TitleAbstractBase, SlugAbstractBase):
    """ Base class for Menu items """
    
    visible = models.BooleanField(verbose_name=_('visible'),
                                  default=True, db_index=True)
    page = models.ForeignKey(Page, null=True, blank=True)
    
    class Meta:
        abstract = True


class Menu(MenuBase):
    """ Main menu """

    ordering = models.SmallIntegerField(verbose_name=_('ordering'),
                                        default=lambda: get_next_ordering(Menu),
                                        db_index=True)
    
    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')
        ordering = ['ordering', ]
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('menu', urlconf='simplesite.urls',
                       kwargs={'menu_slug':self.slug})


class Submenu(MenuBase):
    """ Submenu, related to main menu item """
    
    ordering = models.SmallIntegerField(verbose_name=_('ordering'),
                                        default=lambda: get_next_ordering(Submenu),
                                        db_index=True)
    
    class Meta:
        verbose_name = _('submenu item')
        verbose_name_plural = _('submenu items')
        ordering = ['ordering', ]
    
    menu = models.ForeignKey(Menu)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('submenu', urlconf='simplesite.urls',
                       kwargs={'menu_slug':self.menu.slug,
                               'submenu_slug':self.slug})

