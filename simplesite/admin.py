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
    
class BaseMenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('title',)

    def admin_page(self, obj):
        if obj.page:
            return '<a href="../page/%d/">%s</a>' % (obj.page.id, obj.page)
        else:
            return ''
    admin_page.short_description = Page._meta.verbose_name
    admin_page.allow_tags = True
    
    
class MenuAdmin(BaseMenuAdmin):
    list_display = ('ordering', 'title', 'slug', 'admin_page', 'admin_submenu')
    list_filter = ('visible', )

    def admin_submenu(self, obj):
        if obj.submenu_set.exists():
            return u'<a href="../submenu/?menu__id__exact=%d">%s</a>' \
                % (obj.id, Submenu._meta.verbose_name_plural.capitalize())
        else:
            return ''
    admin_submenu.short_description = ''
    admin_submenu.allow_tags = True
    
class SubmenuAdmin(BaseMenuAdmin):
    list_display = ('ordering', 'title', 'slug', 'admin_page', 'admin_menu')
    list_filter = ('visible', 'menu', )
     
    def admin_menu(self, obj):
        return u'<a href="../menu/%d/">%s</a>' % (obj.menu.id, obj.menu)
    admin_menu.short_description = Menu._meta.verbose_name
    admin_menu.allow_tags = True


admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Submenu, SubmenuAdmin)
