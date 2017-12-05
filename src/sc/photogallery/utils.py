# -*- coding: utf-8 -*-


def last_modified(context):
    """Return the date of the most recently modified object in a container."""
    # we don't care with recursion
    objects = context.objectValues()
    # take all modification dates in seconds since epoch
    modified = [int(obj.modified().strftime('%s')) for obj in objects]
    # XXX: do we really need to take care of the container itself?
    modified.append(int(context.modified().strftime('%s')))
    modified.sort()
    # return the most recent date
    return modified[-1]
