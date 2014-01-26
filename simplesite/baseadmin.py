import logging

logger = logging.getLogger('simplesite')

from django.conf import settings
from django.core.urlresolvers import reverse

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin
from django.contrib.sitemaps import ping_google
from django.conf.urls import patterns, url

from tinymce.widgets import TinyMCE
from tinymce.views import render_to_image_list, render_to_link_list

from sorl.thumbnail import get_thumbnail

from utils import ExtendibleModelAdminMixin
from forms import MenuAdminForm
from models import Page
from settings import PAGEIMAGE_SIZE


class BasePageAdmin(admin.ModelAdmin, ExtendibleModelAdminMixin):
    """ Base class for PageAdmin with things in common for both the
        multilingual as well as the 'normal' branch.

        Note: using relative links to URLs and pages requires the
        setting 'convert_urls' : False for django-tinymce.
    """


    def get_image_list(self, request, object_id):
        """ Get a list of available images for this page for TinyMCE to
            refer to. If the setting exists, scale the image to the default
            size specified in `PAGEIMAGE_SIZE`.
        """
        object = self._getobj(request, object_id)

        page_images = object.pageimage_set.all()

        image_list = []
        for obj in page_images:
            image = obj.image
            if PAGEIMAGE_SIZE:
                image = get_thumbnail(image, PAGEIMAGE_SIZE)

            image_list.append((unicode(obj), image.url))

        return render_to_image_list(image_list)

    def get_link_list(self, request):
        """ Get a list of pages and their URL's.
            TODO: Filter out the current page, if applicable.
        """

        pages = self.model.objects.filter(publish=True)

        # # Exclude the current page, if it exists at all
        # if object.pk:
        #     pages = pages.exclude(pk=object.pk)

        link_list = []
        for page in pages:
            url = page.get_absolute_url()

            if url:
                link_list.append((page.title, url))

        return render_to_link_list(link_list)

    def get_urls(self):
        urls = super(BasePageAdmin, self).get_urls()

        my_urls = patterns('',
            url(r'^(.+)/image_list.js$',
                self._wrap(self.get_image_list),
                name=self._view_name('image_list')),
            url(r'^link_list.js$',
                self._wrap(self.get_link_list),
                name=self._view_name('link_list')),
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

        link_list_url = reverse('admin:simplesite_page_link_list')

        if obj:
            image_list_url = reverse('admin:simplesite_page_image_list',\
                                     args=(obj.pk, ))
            return \
               TinyMCE(mce_attrs={'external_image_list_url': image_list_url,
                                  'external_link_list_url': link_list_url})
        else:
            return \
               TinyMCE(mce_attrs={'external_link_list_url': link_list_url})


class BaseMenuAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('slug',)

    def admin_page(self, obj):
        if obj.page:
            return '<a href="../page/%d/">%s</a>' % (obj.page.id, obj.page)
        else:
            return ''
    admin_page.short_description = Page._meta.verbose_name
    admin_page.allow_tags = True

    form = MenuAdminForm

