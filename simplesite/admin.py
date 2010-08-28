from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin

from tinymce.widgets import TinyMCE

from models import Menu, Submenu, Page


class PageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }


class SubmenuInline(admin.StackedInline):
    model = Submenu
    extra = 0
    

class MenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'ordering', 'admin_page')
    inlines = [SubmenuInline, ]

    def admin_page(self, obj):
        if obj.page:
            return '<a href="../page/%d/">%s</a>' % (obj.page.id, obj.page)
        else:
            return ''
    admin_page.short_description = _('Page')
    admin_page.allow_tags = True


admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)
