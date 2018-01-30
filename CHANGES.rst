Changelog
=========

There's a frood who really knows where his towel is.

1.0b3 (2018-01-30)
------------------

- Fix brown bag release.
  [hvelarde]


1.0b2 (2018-01-29)
------------------

- Remove indirect dependency on five.grok.
  [hvelarde]

- Add compatibility with Python 3.
  [hvelarde]

- Fix human readable file sizes (fixes `#23 <https://github.com/collective/sc.photogallery/issues/23>`_).
  [hvelarde]

- Process static resources using webpack.
  [rodfersou]

- Fix registration of Photo Gallery views.
  [hvelarde]

- Use HTML entities in Unicode Normalization Form C to avoid warnings when validating.
  [hvelarde]


1.0b1 (2016-03-15)
------------------

- Remove hard dependency on plone.app.referenceablebehavior as Archetypes is no longer the default framework in Plone 5.
  Under Plone < 5.0 you should now explicitly add it to the `eggs` part of your buildout configuration to avoid issues while upgrading.
  [hvelarde]

- Avoid photo distorting when landscape format is used.
  [rodfersou]

- The Photo Gallery content type now includes a new `allow_download` field to restrict the downloading of images on an item (closes `#24`_).
  [hvelarde]

- Add Brazilian Portuguese and Spanish translations.
  [hvelarde]

- Make control panel configlet accesible to Site Administrator role (closes `#20`_).
  [hvelarde]

- Add download functionality to Photo Gallery;
  if enabled, users will be able to easily download original images by using an explicit link.
  If ``ftw.zipexport`` is installed, they will be also able to download a ZIP file containing all images (closes `#14`_).
  [rodfersou, hvelarde]

- Implement lead image to be used in folder and collection views (closes `#17`_).
  [hvelarde]

- Load Cycle2 resources from the JS registry if available (closes `#10`_).
  [hvelarde]

- Add Photo Gallery tile for collective.cover.
  [rodfersou, hvelarde]

- Remove dependency on five.grok (closes `#7`_).
  [hvelarde]

- Update template with carousel pager and more layout control (closes `#4`_).
  [rodfersou, agnogueira]

- Drop support for Plone 4.2.
  [hvelarde]

- A Photo Gallery can now be set as the default page view on a container (closes `#1`_).
  [hvelarde]


1.0a1 (2014-08-04)
------------------

- Initial release.

.. _`#1`: https://github.com/collective/sc.photogallery/issues/1
.. _`#4`: https://github.com/collective/sc.photogallery/issues/4
.. _`#7`: https://github.com/collective/sc.photogallery/issues/7
.. _`#10`: https://github.com/collective/sc.photogallery/issues/10
.. _`#14`: https://github.com/collective/sc.photogallery/issues/14
.. _`#17`: https://github.com/collective/sc.photogallery/issues/17
.. _`#20`: https://github.com/collective/sc.photogallery/issues/20
.. _`#24`: https://github.com/collective/sc.photogallery/issues/24
