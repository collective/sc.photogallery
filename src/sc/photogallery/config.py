# -*- coding: utf-8 -*-
import pkg_resources


PROJECTNAME = 'sc.photogallery'

HAS_ZIPEXPORT = True
try:
    pkg_resources.get_distribution('ftw.zipexport')
except pkg_resources.DistributionNotFound:
    HAS_ZIPEXPORT = False
