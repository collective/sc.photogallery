# -*- coding: utf-8 -*-
from sc.photogallery.testing import INTEGRATION_TESTING

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
        """Return the upgrade step that matches with the title specified.

        :param title: the title used to register the upgrade step
        :type title: str
        :returns: an upgrade step or None if there is no match
        :rtype: dict
        """
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        print type(steps[0])
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        :param title: the step we want to run
        :type title: dict
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
        self.assertEqual(self._get_registered_steps, 3)
