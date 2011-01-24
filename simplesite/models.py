import logging
logger = logging.getLogger(__name__)

from django.db import models

from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField

from metadata.models import DateAbstractBase, \
                            TitleAbstractBase, \
                            SlugAbstractBase

from multilingual_model.models import MultilingualModel, \
                                      MultilingualTranslation


class PageTranslation(MultilingualTranslation, TitleAbstractBase):
    class Meta:
        unique_together = ('parent', 'language_code')

    parent = models.ForeignKey('Page', related_name='translations')
    content = models.TextField(verbose_name=_('content'))


class Page(MultilingualModel, DateAbstractBase):
    """ Class representing a page with title and contents """

    publish = models.BooleanField(verbose_name=_('publish'),
                                  default=True, db_index=True)
    
    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    def get_absolute_url(self):
        """ Yield the first related menu item. """
        
        if not self.publish:
            return None

        if self.menu_set.exists():
            return self.menu_set.all()[0].get_absolute_url()
        
        if self.submenu_set.exists():
            return self.submenu_set.all()[0].get_absolute_url()
    
    def __unicode__(self):
        return self.unicode_wrapper('title')


class PageImage(TitleAbstractBase):
    """ Image related to a page. """
    
    page = models.ForeignKey(Page, verbose_name=_('page'))
    image = ImageField(verbose_name=_('image'), upload_to='page_images')


def get_next_ordering(cls):
    ordering = cls.objects.aggregate(models.Max('ordering'))['ordering__max']
    if ordering:
        return ordering+10
    else:
        return 10


class MenuBase(MultilingualModel, SlugAbstractBase):
    """ Base class for Menu items """

    visible = models.BooleanField(verbose_name=_('visible'),
                                  default=True, db_index=True,
                                  help_text=_('Show in menu listings?'))
    page = models.ForeignKey(Page, null=True, blank=True,
                             verbose_name=_('page'))

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.unicode_wrapper('title')



class MenuTranslation(MultilingualTranslation, TitleAbstractBase):
    class Meta:
        unique_together = ('parent', 'language_code')

    parent = models.ForeignKey('Menu', related_name='translations')


class Menu(MenuBase):
    """ Main menu """

    ordering = models.SmallIntegerField(verbose_name=_('ordering'),
                                        default=lambda: get_next_ordering(Menu),
                                        db_index=True)

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')
        ordering = ['ordering', ]
        unique_together = ('slug',)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('menu', urlconf='simplesite.urls',
                       kwargs={'menu_slug':self.slug})


class SubmenuTranslation(MultilingualTranslation, TitleAbstractBase):
   class Meta:
       unique_together = ('parent', 'language_code')

   parent = models.ForeignKey('Submenu', related_name='translations')


class Submenu(MenuBase):
    """ Submenu, related to main menu item """

    ordering = models.SmallIntegerField(verbose_name=_('ordering'),
                                        default=lambda: get_next_ordering(Submenu),
                                        db_index=True)

    class Meta:
        verbose_name = _('submenu item')
        verbose_name_plural = _('submenu items')
        ordering = ['ordering', ]
        unique_together = ('slug', 'menu')

    menu = models.ForeignKey(Menu, verbose_name=_('parent menu'))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('submenu', urlconf='simplesite.urls',
                       kwargs={'menu_slug':self.menu.slug,
                               'submenu_slug':self.slug})

