## Controlled Python Script "update_display_script"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFPlone import PloneMessageFactory as _
context.updateDisplay()

context.plone_utils.addPortalMessage(_(u'Character updated'))
return state.set(status='success')