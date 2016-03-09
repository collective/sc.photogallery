# -*- coding: utf-8 -*-
"""Setup of test for the package.

Prepare test fixtures; note that in Plone >= 5.0 we need to manually
install the desired content types.

We install collective.cover to test the availibility and features of
the tile included for that package.
"""
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from sc.photogallery.config import HAS_ZIPEXPORT

import os
import shutil


PLONE_VERSION = api.env.plone_version()
IMAGES = [
    '640px-Mandel_zoom_00_mandelbrot_set.jpg',
    '640px-Mandel_zoom_04_seehorse_tail.jpg',
    '640px-Mandel_zoom_06_double_hook.jpg',
    '640px-Mandel_zoom_07_satellite.jpg',
    '640px-Mandel_zoom_12_satellite_spirally_wheel_with_julia_islands.jpg'
]


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if PLONE_VERSION >= '5.0':
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)
        else:
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
        if PLONE_VERSION >= '5.0':
            self.applyProfile(portal, 'plone.app.contenttypes:default')
        else:
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
    bases=(FIXTURE,),
    name='sc.photogallery:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='sc.photogallery:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='sc.photogallery:Robot',
)
