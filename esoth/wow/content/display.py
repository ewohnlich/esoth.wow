# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes import ATCTMessageFactory as _
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent, registerATCT
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.CMFCore.utils import getToolByName
from esoth.wow.config import PROJECTNAME
from esoth.wow.interfaces import IWoWDisplay
from zope.interface import implements

WoWDisplaySchema = ATContentTypeSchema.copy() + Schema((
    LinesField('group',
        widget = LinesWidget(
            label= u'Group'),
    ),
    StringField('guild',
        widget = StringWidget(
            label= u'Guild'),
    ),
    StringField('server',
        widget = StringWidget(
            label= u'Server'),
    ),
))

class WoWDisplay(ATCTContent):
    schema = WoWDisplaySchema
    implements(IWoWDisplay)

    security = ClassSecurityInfo()
    
    def players(self):
      cat = getToolByName(self, 'portal_catalog')
      group = self.getGroup()
      guild = self.getGuild()
      server = self.getServer()
      sfilter = {'object_provides':'esoth.wow.content.gearpath.IGearPath','sort_on':'sortable_title'}
      if group:
        sfilter['groups'] = group
      if guild:
        sfilter['guild'] = guild
      if server:
        sfilter['server'] = server
      results = cat(sfilter)
      return results
    
    security.declarePublic('updateDisplay')
    def updateDisplay(self):
      """ update! """
      for player in self.players():
        o=player.getObject()
        o.updateData()
      return self()

registerATCT(WoWDisplay, PROJECTNAME)