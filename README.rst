*************
Photo Gallery
*************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A Photo Gallery content type with a slideshow view.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/sc.photogallery.svg
    :target: https://pypi.python.org/pypi/sc.photogallery

.. image:: https://img.shields.io/travis/collective/sc.photogallery/master.svg
    :target: http://travis-ci.org/collective/sc.photogallery

.. image:: https://img.shields.io/coveralls/collective/sc.photogallery/master.svg
    :target: https://coveralls.io/r/collective/sc.photogallery

These are some sites using ``sc.photogallery``:

* `Portal Brasil 2016 <http://www.brasil2016.gov.br/>`_ (BR)

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/sc.photogallery/issues

Known issues
------------

* `ZIP functionality doesn't seem to support Dexterity based images <https://github.com/collective/sc.photogallery/issues/37>`_.

See the `complete list of bugs on GitHub <hhttps://github.com/collective/sc.photogallery/labels/bug>`_.

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        sc.photogallery

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``Photo Gallery`` and click the 'Activate' button.

.. Note::
    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.

Usage
-----

Original images in a Photo Gallery can be easily downloaded by enabling the display of an explicit link.
To use this feature, go to the Photo Gallery control panel configlet and select 'Enable download?'.

If `ftw.zipexport`_ is installed, you will also be able to download all images on a ZIP file.

.. _`ftw.zipexport`: https://pypi.python.org/pypi/ftw.zipexport

Internals
---------

``Photo Gallery`` uses Cycle2 slideshow plugin for jQuery and it can load its resources from the Plone JS registry if they are present there.

If you're using ``Photo Gallery`` with other packages that use Cycle2 also (like `collective.nitf`_ or `covertile.cycle2`_),
it is highly recommended that you register those resources to load them once and avoid conflicts.

You can use a ``jsregistry.xml`` file that includes the following:

.. code-block:: xml

    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />
    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.carousel.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />
    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />

.. _`collective.nitf`: https://pypi.python.org/pypi/collective.nitf
.. _`covertile.cycle2`: https://pypi.python.org/pypi/covertile.cycle2

Not Entirely Unlike
===================

`collective.plonetruegallery`_
    A gallery/slideshow product for Plone that can aggregate from Picasa and Flickr or use Plone images.

.. _`collective.plonetruegallery`: https://pypi.python.org/pypi/collective.plonetruegallery
