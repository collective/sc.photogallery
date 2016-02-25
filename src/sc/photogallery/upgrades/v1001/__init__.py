# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from sc.photogallery.config import PROJECTNAME
from sc.photogallery.interfaces import IPhotoGallery

import logging


logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Register JS resources, configlet fields and update type information."""
    profile = 'profile-sc.photogallery.upgrades.v1001:default'
    loadMigrationProfile(context, profile)
    logger.info(u'JS resources registered')


def cook_javascript_resources(context):
    """Cook JS resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('JS resources were cooked')


def update_catalog(context):
    """Update Photo Gallery objects as class information has changed."""
    logger.info(u'Updating Photo Gallery objects')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(object_provides=IPhotoGallery.__identifier__)
    logger.info(u'{0} objects found'.format(len(results)))
    # use a generator to save memory
    results = (i.getObject() for i in results)
    for obj in results:
        obj.reindexObject()
    logger.info(u'Catalog successfully updated')


def update_configlet(setup_tool):
    """Update control panel configlet."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'controlpanel')
    logger.info('Control panel configlet updated.')
