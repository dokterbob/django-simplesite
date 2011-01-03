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

TODO
----
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
