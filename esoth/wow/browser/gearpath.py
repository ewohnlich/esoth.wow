from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from esoth.wow.content.gear import slot, gear, boss
boss=boss.copy()
gear=gear.copy()
slot=slot.copy()
        
class GearPathView(BrowserView):
  def __call__(self,action='',item=''):
    if action and item:
      slot = gear[item]['slot']
      if action == 'equip':
        slot = slot.lower()
        setattr(self.context,slot,item)
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