=================
django-simplesite
=================
A simple pseudo-static site app with menu, submenu and pages.
-------------------------------------------------------------

Features
========
* A decoupling of navigational structure and content - this allows for setting
  up a menu/submenu structure for which some menu's and submenu's might refer
  to other app's views and some might refer to 'pages' in simplesite.
* Validation of navigational structure: when creating menu or submenu object,
  the validity of the resulting URI's is automatically validated, preventing
  the creation of broken links.
* Rather than implementing a full tree structure, a 2-level menu/submenu
  hierarchy has been chosen as to maintain simplicity and to help content
  managers by forcing them to make data accessible using a minimal
  amount of navigation.
* Fully integrated TinyMCE WYSIWYG-editor using the `django-tinymce <http://code.google.com/p/django-tinymce/>`_ package.
* Inline image support and cross-linking pages from within TinyMCE.
* A `SimplesiteFallbackMiddleware` allowing for simplesite to be used
  similar to the `FlatpageFallbackMiddleWare <https://docs.djangoproject.com/en/1.3/ref/contrib/flatpages/#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware>`_ of Django's own flatpages. This allows one to override specific parts of the URI space which would otherwise be covered by other apps.
* A `menu` RequestContext processor making a menu- and submenu-list and 
  with it the current page available in the request context.
* Fully translatable content using the `django-multilingual-model <https://github.com/dokterbob/django-multilingual-model>`_ app.
* A simple mechanism allowing for template overrides for specific menu's or
  submenu's.


Requirements
============
Please refer to `requirements.txt <http://github.com/dokterbob/django-simplesite/blob/master/requirements.txt>`_ for an updated list of required packes.

Installation
============
#)  Install the package and its dependencies straight from Github and link
    them into your `PYTHONPATH`::

	pip install -e git+http://github.com/dokterbob/django-metadata.git#egg=django-metadata \
	    -e git+http://github.com/dokterbob/django-multilingual-model.git#egg=django-multilingual-model \
	    -e git+http://github.com/dokterbob/django-simplesite.git@multilingual-model#egg=django-simplesite \ 

    (In either case it is recommended that you use 
    `VirtualEnv <http://pypi.python.org/pypi/virtualenv>`_ in order to
    keep your Python environment somewhat clean.)

#)  Add simplesite and to ``INSTALLED_APPS`` in settings.py and make sure that
    the dependencies django-tinymce and django-extensions are there as well::

	INSTALLED_APPS = (
	    ...
	    'metadata',
	    'multilingual_model',
	    ...
	    'simplesite',
	    ...
	)

#)  Update the database structure::

	./manage.py syncdb 

#)  Add the `menu` context processor to Django's default
    `TEMPLATE_CONTEXT_PROCESSORS`::

	TEMPLATE_CONTEXT_PROCESSORS = (
	    ...
	    'simplesite.context_processors.menu',
	    ...
	)    

    This will make the following variables available from within
    any view using a `RequestContext <https://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext>`_ for template rendering:

    *   `page_current`: the current `Page` object
    *   `menu_current`: the `Menu` object pertaining to the current page
    *   `submenu_current`: the `Submenu` object pertaining to the current page

#)  Setup the `SimplesiteFallbackMiddleware` to go and look for a page related
    to the menu whenever a 404 is raised::

	MIDDLEWARE_CLASSES = (
	    ...
	    'simplesite.middleware.SimplesiteFallbackMiddleware',
	)

    Note that the order of `MIDDLEWARE_CLASSES` matters. Generally, you can
    put `SimplesiteFallbackMiddleware` at the end of the list, because it’s a    
    last resort.

    Alternately, you can simply use simplesite's page view directly from your
    `urls.py` by adding the following line::

	urlpatterns = patterns('',
	    ...
	    (r'^', include('simplesite.urls'))
	)

    Make sure you add this line at the end of your `urlpatterns`, otherwise it
    will make all other URI's inaccessible.

#)  Setup (at least) the page template `simplesite/page.html`, which receives
    the context variables from the `RequestContext` described above.

#)  Optionally, override the basic page template for menu's and submenu's,
    according to the following template::

	templates/simplesite/<menu_slug>/page.html
	templates/simplesite/<menu_slug>/<submenu_slug>/page.html


TODO
====
* Add one additional level of navigational depth, a 'subsubmenu'.
* Add a setting for excluding certain URL patterns (ie. static files)
  from the simplesite middleware.
* Make all elements produced by the `RequestContextProcessor` lazy so we never
  produce redundant database hits.
* Write unittests for both master as well as the multilingual-model branches.
* Find a workflow in which merging of multilingual and master branches becomes
  a lot easier.
* PEP8 cleanup.
* Write decent documentation.
* Add image size to `<img>` tags produced by TinyMCE.
