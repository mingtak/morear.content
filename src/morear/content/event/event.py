# -*- coding: utf-8 -*-
from plone import api
import transaction


def userLoginToFolderContents(event):
    if api.user.is_anonymous():
        return
    portal = api.portal.get()
    current = api.user.get_current()
#    if api.user.has_permission('Modify portal content', user=current):
    if api.user.has_permission('Add portal content', user=current) or \
       api.user.has_permission('Review portal content', user=current):
        portal.REQUEST.response.redirect('%s/folder_contents' % portal.absolute_url())


def moveContentToTop(item, event):
    """ Moves Item to the top of its folder """
    try:
        folder = item.getParentNode()
    except:
        return

    if not hasattr(folder, 'moveObjectsToTop'):
        return

    if item.portal_type in ['News Item']:
        try:
            folder.moveObjectsToTop(item.id)
        except:pass


def toFolderContents(item, event):
    try:
        portal = api.portal.get()
    except:return
    try:
        parent = item.getParentNode()
    except:
        portal.REQUEST.response.redirect('%s/folder_contents' % portal.absolute_url())

    try:
        if item.Type() in ['Image', 'File']:
            return
        if item.Type() == 'Folder':
            item.REQUEST.response.redirect('%s/folder_contents' % item.absolute_url())
        else:
            item.REQUEST.response.redirect('%s/folder_contents' % parent.absolute_url())
    except:
        portal.REQUEST.response.redirect('%s/folder_contents' % portal.absolute_url())


def addCancelToFolderContents(item, event):
    item.REQUEST.response.redirect('%s/folder_contents' % item.absolute_url())


def checkpType(item, event):
    if item.pType == 'headphone':
        if not (item.driver and item.lineLength and item.surfaceColorR and item.surfaceColorL):
            api.portal.show_message(message='Wrong, Please fill all fields in headphone tab!', request=item.REQUEST, type='warning')

    if item.pType == 'earplugs':pass
