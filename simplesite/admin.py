import logging

logger = logging.getLogger('simplesite')

from sorl.thumbnail.admin import AdminInlineImageMixin

from django.conf import settings
from django.core.urlresolvers import reverse

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin
from django.contrib.sitemaps import ping_google
from django.conf.urls import patterns, url

from models import Menu, Submenu, Page, PageImage, MenuTranslation, \
                   SubmenuTranslation, PageTranslation
from baseadmin import BasePageAdmin, BaseMenuAdmin, TinyMCEAdminMixin

from multilingual_model.admin import TranslationInline


class PageTranslationInline(TinyMCEAdminMixin, TranslationInline):
    model = PageTranslation

    def get_formset(self, request, obj=None, **kwargs):
        """ Override the form widget for the content field with a TinyMCE
            field which uses a dynamically assigned image list. """

        formset = super(TinyMCEAdminMixin, self).get_formset(request, obj=None, **kwargs)

        formset.form.base_fields['content'].widget = self.get_tinymce_widget(obj)

        return formset


class PageImageInline(AdminInlineImageMixin, admin.TabularInline):
    model = PageImage
    extra = 1


class PageAdmin(BasePageAdmin):
    inlines = (PageTranslationInline, PageImageInline, )
    list_display = ('admin_title', 'publish')

    def admin_title(self, obj):
        return unicode(obj)
    admin_title.short_description = _('title')


class MenuTranslationInline(TranslationInline):
    model = MenuTranslation


class SubmenuTranslationInline(TranslationInline):
    model = SubmenuTranslation


class MenuAdmin(BaseMenuAdmin):
    list_display = ('ordering', 'slug', 'visible', 'admin_page', 'admin_submenu')
    list_filter = ('visible', )

    def admin_submenu(self, obj):
        if obj.submenu_set.exists():
            return u'<a href="../submenu/?menu__id__exact=%d">%s</a>' \
                % (obj.id, Submenu._meta.verbose_name_plural.capitalize())
        else:
            return ''
    admin_submenu.short_description = ''
    admin_submenu.allow_tags = True

    inlines = [MenuTranslationInline, ]


class SubmenuAdmin(BaseMenuAdmin):
    list_display = ('ordering', 'slug', 'visible', 'admin_page', 'admin_menu')
    list_filter = ('visible', 'menu', )

    def admin_menu(self, obj):
        return u'<a href="../menu/%d/">%s</a>' % (obj.menu.id, obj.menu)
    admin_menu.short_description = Menu._meta.verbose_name
    admin_menu.allow_tags = True

    inlines = [SubmenuTranslationInline, ]


admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Submenu, SubmenuAdmin)
