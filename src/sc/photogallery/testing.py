# -*- coding: utf-8 -*-
"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.

Tile for collective.cover is only tested in Plone 4.3.
"""
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from sc.photogallery.config import HAS_ZIPEXPORT

import os
import pkg_resources
import shutil


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
    HAS_DEXTERITY = False
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
    HAS_DEXTERITY = True

try:
    pkg_resources.get_distribution('collective.cover')
except pkg_resources.DistributionNotFound:
    HAS_COVER = False
else:
    HAS_COVER = True


IS_PLONE_5 = api.env.plone_version().startswith('5')
IMAGES = [
    '640px-Mandel_zoom_00_mandelbrot_set.jpg',
    '640px-Mandel_zoom_04_seehorse_tail.jpg',
    '640px-Mandel_zoom_06_double_hook.jpg',
    '640px-Mandel_zoom_07_satellite.jpg',
    '640px-Mandel_zoom_12_satellite_spirally_wheel_with_julia_islands.jpg',
]


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if HAS_COVER:
            import collective.cover
            self.loadZCML(package=collective.cover)

        if HAS_ZIPEXPORT:
            import ftw.zipexport
            self.loadZCML(package=ftw.zipexport)

        import collective.js.cycle2
        self.loadZCML(package=collective.js.cycle2)

        import sc.photogallery
        self.loadZCML(package=sc.photogallery)

    def setUpPloneSite(self, portal):
        if HAS_COVER:
            self.applyProfile(portal, 'collective.cover:default')

        if HAS_ZIPEXPORT:
            self.applyProfile(portal, 'ftw.zipexport:default')

        self.applyProfile(portal, 'collective.js.cycle2:default')
        self.applyProfile(portal, 'sc.photogallery:default')

        current_dir = os.path.abspath(os.path.dirname(__file__))
        for img in IMAGES:
            img_path = os.path.join(current_dir, 'tests', img)
            shutil.copy2(img_path, '/tmp')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='sc.photogallery:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='sc.photogallery:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='sc.photogallery:Robot',
)
