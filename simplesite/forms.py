import logging

from django import forms

from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import resolve, Resolver404

from simplesite.views import page as page_view

logger = logging.getLogger('simplesite')

class MenuAdminForm(forms.ModelForm):
    def clean(self):
        page = self.cleaned_data['page']
        
        if not page:
            slug = self.cleaned_data['slug']
            
            if 'menu' in self.cleaned_data:                
                menu = self.cleaned_data['menu']
                path = '/%s/' % menu.slug
            else:
                path = '/'
            
            path += '%s/' % slug
            
            logger.debug('Checking whether the path %s yields a view in the URL space.' % path)

            # This should always work.
            try:
                view, args, kwargs = resolve(path)
            except Resolver404:
                raise forms.ValidationError(_('Without a page, this menu \
                        item would point nowhere. Please select a page for it \
                        to link to.'))
        
        return super(MenuAdminForm, self).clean()
        

