from django.conf.urls.defaults import *

from simplesite.urls import urlpatterns as simplesite_urlpatterns

urlpatterns = patterns('simplesite.tests.testapp.views',
    (r'^myview/$', 'myview'),
)

urlpatterns += simplesite_urlpatterns
