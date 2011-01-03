from django.contrib.sitemaps import Sitemap
from simplesite.models import Menu, Submenu


class MenuSitemap(Sitemap):
    def items(self):
        return Menu.objects.filter(visible=True)


class SubmenuSitemap(Sitemap):
    def items(self):
        return Submenu.objects.filter(visible=True)


class PageSitemap(Sitemap):
    def lastmod(self, item):
        return item.page.modify_date

    def items(self):
        return Menu.objects.filter(page__isnull=False, page__publish=True)
