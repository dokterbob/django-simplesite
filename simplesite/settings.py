from django.conf import settings

PAGEIMAGE_SIZE = getattr(settings, 'SIMPLESITE_PAGEIMAGE_SIZE', None)
IGNORE_PATHS = getattr(settings, 'SIMPLESITE_IGNORE_PATHS', ())

