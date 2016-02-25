# -*- coding: utf-8 -*-
import pkg_resources


PROJECTNAME = 'sc.photogallery'

# Cycle2 JS resources used by the package
JS_RESOURCES = (
    '++resource++collective.js.cycle2/jquery.cycle2.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.carousel.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js',
)

HAS_ZIPEXPORT = True
try:
    pkg_resources.get_distribution('ftw.zipexport')
except pkg_resources.DistributionNotFound:
    HAS_ZIPEXPORT = False
