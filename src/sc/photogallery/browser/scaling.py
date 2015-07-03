# -*- coding: utf-8 -*-
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling


# XXX: compatibility with summary_view in collections
#      this probably should not be necessary if we can define the image
#      method of the class as a property
class ImageScaling(BaseImageScaling):

    """Adapter for image fields that allows generating scaled images."""

    def scale(self, fieldname=None, scale=None, height=None, width=None, **parameters):
        """Override ofiginal scale method so we can return an image scale."""

        if fieldname == 'image':
            image = self.context.image()
            scales = image.restrictedTraverse('@@images')
            return scales.scale(fieldname, scale, height, width, **parameters)
        else:
            return super(
                ImageScaling, self).scale(fieldname, scale, height, width, **parameters)
