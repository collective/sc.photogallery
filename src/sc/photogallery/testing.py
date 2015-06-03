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

PLONE_VERSION = api.env.plone_version()


def turn_off_referenceablebehavior():
    """FIXME"""
    from plone.dexterity.interfaces import IDexterityFTI
    from zope.component import queryUtility
    fti = queryUtility(IDexterityFTI, name='Photo Gallery')
    behaviors = list(fti.behaviors)
    behaviors.remove('plone.app.referenceablebehavior.referenceable.IReferenceable')
    fti.behaviors = tuple(behaviors)


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if PLONE_VERSION >= '5.0':
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)
        else:
            import collective.cover
            self.loadZCML(package=collective.cover)

        import sc.photogallery
        self.loadZCML(package=sc.photogallery)

    def setUpPloneSite(self, portal):
        if PLONE_VERSION >= '5.0':
            self.applyProfile(portal, 'plone.app.contenttypes:default')
        else:
            self.applyProfile(portal, 'collective.cover:default')

        self.applyProfile(portal, 'sc.photogallery:default')

        if PLONE_VERSION >= '5.0':
            turn_off_referenceablebehavior()

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
