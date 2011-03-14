import logging

from django import forms

from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import resolve, Resolver404

logger = logging.getLogger('simplesite')


class MenuAdminForm(forms.ModelForm):
    def clean_page(self):
        # When form fields don't validate, they won't end up in
        # cleaned_data, hence we should account for them not to
        # be there.
        page = self.cleaned_data.get('page', None)
        slug = self.cleaned_data.get('slug', None)

        if not page and slug:
            menu = self.cleaned_data.get('menu', None)
            if menu:
                path = '/%s/' % menu.slug
            else:
                path = '/'

            path += '%s/' % slug

            logger.debug('Checking whether the path %s yields a view in \
                          the URL space.', path)

            # This should always work.
            try:
                view, args, kwargs = resolve(path)
            except Resolver404:
                raise forms.ValidationError(_('Without a page, this menu \
                        item would point nowhere. Please select a page for it \
                        to link to.'))


