from surlex.dj import surl

from django.conf.urls import patterns


urlpatterns = patterns('simplesite.views',
    surl(r'^<menu_slug:s>/<submenu_slug:s>/', 'page', name='submenu'),
    surl(r'^<menu_slug:s>/', 'page', name='menu'),
)

