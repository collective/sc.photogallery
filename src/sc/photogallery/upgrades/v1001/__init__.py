# -*- coding: utf-8 -*-
from sc.photogallery.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    """Updates package to profile version 1001."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-sc.photogallery.upgrades.v1001:default'
    loadMigrationProfile(context, profile)
    logger.info('Profile updated to version 1001')
