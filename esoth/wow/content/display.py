from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from plone.dexterity.content import Item
from zope.interface import implements

from five import grok

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

class UpdateDisplay(grok.View):
    grok.name('armory')
    grok.context(ICharDisplay)
    
    def render(self):
      self.context.updateDisplay()
      
      IStatusMessage(self.request).addStatusMessage(_(u"Roster updated"),"info")
      self.request.response.redirect(self.context.absolute_url())