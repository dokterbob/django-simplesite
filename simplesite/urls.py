from surlex.dj import surl

from .views import page


urlpatterns = [
    surl(r'^<menu_slug:s>/<submenu_slug:s>/', page, name='submenu'),
    surl(r'^<menu_slug:s>/', page, name='menu'),
]
