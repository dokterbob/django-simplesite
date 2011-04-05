=================
django-simplesite
=================

A simple pseudo-static site app with menu, submenu and pages.

Features
--------
* Fully integrated with TinyMCE using the `django-tinymce` package.
* Inline image support and cross-linking pages from within TinyMCE.
* A `SimplesiteFallbackMiddleware` allowing for simplesite to be used
  similar to Django's own flatpages app.
* A `menu` RequestContextProcessor making a menu- and submenu-list and with it
  the current page available in the request context.
* All content is fully and transparently translatable to any number of languages, using the `django-multilingual-model` application.

Requirements
------------
Please refer to `requirements.txt <http://github.com/dokterbob/django-newsletter/blob/master/requirements.txt>`_ for an updated list of required packes.

Installation
------------
#)  First of all it is recommended that you use 
    `VirtualEnv <http://pypi.python.org/pypi/virtualenv>`_ in order to
    keep your Python environment somewhat clean. Wihtin your environment, it
    is easy to install `django-simplesite` straight from GitHub::
    
        pip install -e https://github.com/dokterbob/django-simplesite.git#egg=simplesite

#)  Make sure all dependencies, as mentioned in `requirements.txt` are
    installed.

#)  Add `simplesite` to `INSTALLED_APPS` in `settings.py` and make sure that
    the dependencies `django-tinymce` and `django-multilingual-model` are   
    there as well::
    
	INSTALLED_APPS = (
	    ...
	    'tinymce',
	    'sorl.thumbnail',
	    ...
	    'simplesite',
	    ...
	)

#)  Add the fallback middleware to `MIDDLEWAER_CLASSES` in `settings.py`, so
    404 errors will be caught (similar to Django's native 
    `flatpages  app <http://docs.djangoproject.com/en/dev/ref/contrib/flatpages/>`_)::

	MIDDLEWARE_CLASSES = (
		...
		'simplesite.middleware.SimplesiteFallbackMiddleware',
		...
	)

#) In order to have the menu/submenu structure available in every template
   rendered with a `RequestContext <http://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext>`_, 
   add the simplesite menu context processor.

   This exposes the following context variables in your template's context:
    
    * `menu_current`: The current menu (if any)
    * `submenu_current`: The current submenu (if any)
    * `menu_list`: A list of visible main menu items
    * `submenu_list`: A list of visible submenu items for the current menu
   
   To enable this context processor, make sure it's listed in  `TEMPLATE_CONTEXT_PROCESSORS` in `settings.py`::

	TEMPLATE_CONTEXT_PROCESSORS = (
		...
		'simplesite.context_processors.menu',
		...
	)


#) Now you're all setup! 

   From the admin you can now make a menu/submenu
   structure for your site, which can be used to render menu's, breadcrumbs
   and other navigational elements. Also, pages can be associated to menu's
   and submenu's - allowing for an easy way to create semi-static pages
   in your site.

TODO
---- 
* Links lists should refer to menu and submenu items - not to pages. Some little stupid thing I've simply forgotten.
* Add a setting for excluding certain URL patterns (ie. static files)
  from the simplesite middleware.
* Write unittests for both master as well as the multilingual-model branches.
* Find a workflow in which merging of multilingual and master branches becomes
  a lot easier.
* PEP8 cleanup.
* Write better and more documentation.
