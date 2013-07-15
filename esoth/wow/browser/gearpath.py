from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from urllib import urlopen
import json

from esoth.wow.content.gear import getGear

class GearUpdate(BrowserView):
  def __call__(self):
    self.context.updateData()
    
    IStatusMessage(self.request).addStatusMessage(_(u"Character updated"),"info")
    self.request.response.redirect(self.context.absolute_url())
        
class GearPathView(BrowserView):
  def __call__(self,action='',item='',slot=''):
    gear = getGear(self.context.spec)[2]
    if action and item:
      if not slot:
        slot = gear[item]['slot']
      if action == 'equip':
        slot = slot.lower()
        if getattr(self.context,slot) == item:
          setattr(self.context,slot,'')
        else:
          setattr(self.context,slot,item)
        acquiredItems = self.context.acquiredItems or set([])
        if item not in acquiredItems:
          acquiredItems.add(item)
          self.context.acquiredItems = acquiredItems
      elif action == 'acquire':
        acquiredItems = self.context.acquiredItems or set([])
        if item in acquiredItems:
          acquiredItems.remove(item)
        else:
          acquiredItems.add(item)
        self.context.acquiredItems = acquiredItems
      elif action == 'bis':
        bisItems = self.context.bisItems or set([])
        if item in bisItems:
          bisItems.remove(item)
        else:
          bisItems.add(item)
        self.context.bisItems = bisItems
      elif action == 'downgrade':
        downgradeItems = self.context.downgradeItems or set([])
        if item in downgradeItems:
          downgradeItems.remove(item)
        else:
          downgradeItems.add(item)
        self.context.downgradeItems = downgradeItems
    
    template = ZopeTwoPageTemplateFile('gearpath.pt')
    return template(self)
    
class BossTableView(BrowserView):
  """ """
  def bossNeeds(self):
    return self.context.bossNeeds()
  
  def bossOrder(self):
    return self.context.bossOrder()