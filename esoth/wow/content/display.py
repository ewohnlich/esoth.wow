from Products.CMFCore.utils import getToolByName
from plone.dexterity.content import Item
from zope.interface import implements

from esoth.wow.interfaces import ICharDisplay

class WoWDisplay(Item):
    implements(ICharDisplay)
    meta_type = 'WoWDisplay'
    
    def players(self):
      cat = getToolByName(self, 'portal_catalog')
      sfilter = {'object_provides':'esoth.wow.interfaces.IGearPath','sort_on':'sortable_title'}
      if self.groups:
        sfilter['groups'] = list(self.groups)
      if self.guild:
        sfilter['guild'] = self.guild
      if self.server:
        sfilter['server'] = self.server
      results = cat(sfilter)
      return results
    
    def updateDisplay(self):
      """ update! """
      for player in self.players():
        o=player.getObject()
        o.updateData()
      return self()