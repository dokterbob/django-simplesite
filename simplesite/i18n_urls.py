from django.conf.urls.i18n import i18n_patterns

from .urls import urlpatterns

"""
i18n variant of URLConf to allow for the context processors to function when
i18n_patterns are used.
"""
urlpatterns = i18n_patterns(*urlpatterns)
