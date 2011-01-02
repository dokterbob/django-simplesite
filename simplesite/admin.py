import logging

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
from forms import MenuAdminForm
from utils import ExtendibleModelAdminMixin

logger = logging.getLogger('simplesite')


class BasePageAdmin(admin.ModelAdmin, ExtendibleModelAdminMixin):
    def get_image_list(self, request, object_id):
        """ Get a list of available images for this page for TinyMCE to
            refer to.
        """
        object = self._getobj(request, object_id)
        
        images = object.pageimage_set.all()
        image_list = [(unicode(obj), obj.image.url) for obj in images]
        
        return render_to_image_list(image_list)
     
    
    def get_urls(self):
        urls = super(BasePageAdmin, self).get_urls()
        
        my_urls = patterns('',
            url(r'^(.+)/image_list.js$', 
                self._wrap(self.get_image_list), 
                name=self._view_name('image_list')),
        )

        return my_urls + urls

               
    def save_model(self, request, obj, form, change):
        super(BasePageAdmin, self).save_model(request, obj, form, change)
        
        if not settings.DEBUG and obj.publish:
            try:
                ping_google()
            except Exception:
                # Bare 'except' because we could get a variety
                # of HTTP-related exceptions.
                logger.warning('Error pinging Google while saving %s.' \
                                    % obj)
        else:
            logger.debug('Not pinging Google while saving %s, DEBUG=True.' \
                            % obj)


class TinyMCEAdminMixin(object):
    @staticmethod
    def get_tinymce_widget(obj=None):
        """ Return the appropriate TinyMCE widget. """
        if obj:
            image_list_url = reverse('admin:simplesite_page_image_list',\
                                     args=(obj.pk, ))

            return \
               TinyMCE(mce_attrs={'external_image_list_url': image_list_url})
        else:
            return TinyMCE()


    def get_form(self, request, obj=None, **kwargs):
        """ Override the form widget for the content field with a TinyMCE
            field which uses a dynamically assigned image list. """

        print 'belletje b'
        
        form = super(TinyMCEAdminMixin, self).get_form(request, obj=None, **kwargs)
        
        form.base_fields['content'].widget = self.get_tinymce_widget(obj)

        return form


class PageImageInline(AdminInlineImageMixin, admin.TabularInline):
    model = PageImage
    extra = 1


class PageAdmin(TinyMCEAdminMixin, BasePageAdmin):
    inlines = (PageImageInline, )


class SubmenuInline(admin.StackedInline):
    model = Submenu
    extra = 0


class BaseMenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('title',)

    def admin_page(self, obj):
        if obj.page:
            return '<a href="../page/%d/">%s</a>' % (obj.page.id, obj.page)
        else:
            return ''
    admin_page.short_description = Page._meta.verbose_name
    admin_page.allow_tags = True
    
    form = MenuAdminForm
    
    
class MenuAdmin(BaseMenuAdmin):
    list_display = ('ordering', 'title', 'slug', 'visible', 'admin_page', 'admin_submenu')
    list_filter = ('visible', )

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
