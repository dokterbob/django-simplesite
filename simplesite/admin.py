import logging

logger = logging.getLogger('simplesite')

from sorl.thumbnail.admin import AdminInlineImageMixin

from django.conf import settings
from django.core.urlresolvers import reverse

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin
from django.contrib.sitemaps import ping_google
from django.conf.urls.defaults import patterns, url

from tinymce.widgets import TinyMCE
from tinymce.views import render_to_image_list

from sorl.thumbnail.admin import AdminInlineImageMixin

from models import Menu, Submenu, Page, PageImage
from baseadmin import BasePageAdmin, BaseMenuAdmin, TinyMCEAdminMixin


class PageImageInline(AdminInlineImageMixin, admin.TabularInline):
    model = PageImage
    extra = 1


class PageAdmin(TinyMCEAdminMixin, BasePageAdmin):
    inlines = (PageImageInline, )
    list_display = ('page_title','publish',)
    
    def page_title(self, obj):
        return u'%s' % (obj.title)
    page_title.short_description = 'title'
    page_title.allow_tags = True
    

    def get_form(self, request, obj=None, **kwargs):
        """ Override the form widget for the content field with a TinyMCE
            field which uses a dynamically assigned image list. """

        form = super(TinyMCEAdminMixin, self).get_form(request, obj=None, **kwargs)
        
        form.base_fields['content'].widget = self.get_tinymce_widget(obj)

        return form


class SubmenuInline(admin.StackedInline):
    model = Submenu
    extra = 0


class MenuAdmin(BaseMenuAdmin):
    list_display = ('title', 'slug', 'ordering', 'visible', 'admin_page', 'admin_submenu')
    list_filter = ('visible', )
    filter_horizontal = ('images',)

    def admin_submenu(self, obj):
        if obj.submenu_set.exists():
            return u'<a href="../submenu/?menu__id__exact=%d">%s</a>' \
                % (obj.id, Submenu._meta.verbose_name_plural.capitalize())
        else:
            return ''
    admin_submenu.short_description = ''
    admin_submenu.allow_tags = True


class SubmenuAdmin(BaseMenuAdmin):
    list_display = ('ordering', 'title', 'slug', 'visible', 'admin_page', 'admin_menu')
    list_filter = ('visible', 'menu', )
     
    def admin_menu(self, obj):
        return u'<a href="../menu/%d/">%s</a>' % (obj.menu.id, obj.menu)
    admin_menu.short_description = Menu._meta.verbose_name
    admin_menu.allow_tags = True


admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Submenu, SubmenuAdmin)
