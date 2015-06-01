# -*- coding: utf-8 -*-
from plone import api
from sc.photogallery.config import PROJECTNAME
from sc.photogallery.interfaces import IPhotoGallery
from plone.app.upgrade.utils import loadMigrationProfile

import logging
logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Register JS resources and update type information."""
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
    for obj in (i.getObject() for i in results):
        obj.reindexObject()
    logger.info(u'Catalog successfully updated')
