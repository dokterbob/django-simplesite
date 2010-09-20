from django.contrib.sitemaps import Sitemap
from simplesite.models import Menu


class PageSitemap(Sitemap):
    def lastmod(self, item):
        return item.page.modify_date

    def items(self):
        return Menu.objects.filter(page__isnull=False, page__publish=True)
