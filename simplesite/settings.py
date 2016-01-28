from django.conf import settings

PAGEIMAGE_SIZE = getattr(settings, 'SIMPLESITE_PAGEIMAGE_SIZE', None)
URLCONF = getattr(settings, 'SIMPLESITE_URLCONF', 'simplesite.urls')
