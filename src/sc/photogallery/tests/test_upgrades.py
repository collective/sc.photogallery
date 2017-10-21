# -*- coding: utf-8 -*-
from plone import api
from sc.photogallery.testing import INTEGRATION_TESTING
from sc.photogallery.testing import IS_PLONE_5

import unittest


class BaseUpgradeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'sc.photogallery:default'
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step_by_title(self, title):
        """Return the upgrade step that matches the title specified.

        :param title: the title used to register the upgrade step
        :type title: str
        :returns: an upgrade step or None if there is no match
        :rtype: dict
        """
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        :param step: the step we want to run
        :type step: dict
        """
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def _get_registered_steps(self):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class To1001TestCase(BaseUpgradeTestCase):

    def setUp(self):
        BaseUpgradeTestCase.setUp(self, u'1000', u'1001')

    def test_registered_steps(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._get_registered_steps, 4)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
    def test_miscellaneous(self):
        # check if the upgrade step is registered
        title = u'Miscellaneous'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        js_tool = self.portal['portal_javascripts']
        from sc.photogallery.tests.test_setup import JS
        js_tool.unregisterResource(JS)
        self.assertNotIn(JS, js_tool.getResourceIds())

        types_tool = self.portal['portal_types']
        old_klass = 'sc.photogallery.content.photogallery.PhotoGallery'
        new_klass = 'sc.photogallery.content.PhotoGallery'
        types_tool['Photo Gallery'].klass = old_klass
        self.assertEqual(types_tool['Photo Gallery'].klass, old_klass)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertIn(JS, js_tool.getResourceIds())
        self.assertEqual(types_tool['Photo Gallery'].klass, new_klass)

    def test_update_catalog(self):
        # check if the upgrade step is registered
        title = u'Update catalog'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # add an object and modified it without updating the catalog
        with api.env.adopt_roles(['Manager']):
            g1 = api.content.create(self.portal, 'Photo Gallery', 'g1')

        g1.description = 'Foo'
        catalog = self.portal['portal_catalog']
        self.assertEqual(len(catalog(Description='Foo')), 0)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertEqual(len(catalog(Description='Foo')), 1)

    def test_update_configlet(self):
        # check if the upgrade step is registered
        title = u'Update control panel configlet'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        cptool = api.portal.get_tool('portal_controlpanel')
        configlet = cptool.getActionObject('Products/photogallery')
        configlet.permissions = old_permissions = ('cmf.ManagePortal',)
        self.assertEqual(configlet.getPermissions(), old_permissions)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        configlet = cptool.getActionObject('Products/photogallery')
        new_permissions = ('sc.photogallery: Setup',)
        self.assertEqual(configlet.getPermissions(), new_permissions)
