import logging

from django import forms

from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('simplesite')

from django.core.urlresolvers import resolve, Resolver404


class MenuAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data

        # When form fields don't validate, they won't end up in
        # cleaned_data, hence we should account for them not to
        # be there.
        page = cleaned_data.get('page', None)
        slug = cleaned_data.get('slug', None)

        if not page and slug:
            menu = cleaned_data.get('menu', None)
            if menu:
                path = '/%s/' % menu.slug
            else:
                path = '/'

            path += '%s/' % slug

            logger.debug('Checking whether the path %s yields a view.',
                         path)

            # This should always work.
            try:
                view, args, kwargs = resolve(path)
            except Resolver404:
                error_message = \
                    _('Without a page, this menu \
                       item would point nowhere. Please select a page for it \
                       to link to.')
                self._errors['page'] = self.error_class([error_message])

                # Remove invalid data
                del cleaned_data['page']

        return cleaned_data
