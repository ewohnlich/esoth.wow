from five import grok
from plone.directives import form
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile, ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from urllib import urlopen
import json

from esoth.wow.content.gear import getGear
from esoth.wow.content.gearpath import IGearPath

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
    
class ICharacterVerifySchema(form.Schema):
  """ """
    
class CharacterVerify(form.SchemaForm):
  """ Verify that you own a character """
  grok.context(IGearPath)
  grok.require('zope2.View')
  grok.name('character-verify')
  template = ViewPageTemplateFile('verify.pt')
  
  schema = ICharacterVerifySchema
  
  def getSlotsToRemove(self):
    # check if these variables are assigned. If not, get three random slots
    memb = getToolByName(self.context,'portal_membership').getAuthenticatedMember()
    if not memb.getId():
      return []
    current_user = memb.getId()
    if self.context.slotToBlank1 and self.context.verifier == current_user:
      one = self.context.slotToBlank1
      two = self.context.slotToBlank2
      three = self.context.slotToBlank3
    else:
      import random
      from datetime import datetime
      random.seed(datetime.now())
      self.context.verifier = current_user
      slots = ['Weapon','Helm','Neck','Back','Chest','Wrists','Hands','Waist','Legs','Feet']
      one = slots.pop(slots.index(random.choice(slots)))
      self.context.slotToBlank1 = one
      two = slots.pop(slots.index(random.choice(slots)))
      self.context.slotToBlank2 = two
      three = slots.pop(slots.index(random.choice(slots)))
      self.context.slotToBlank3 = three
    return (one,two,three)
  
  @button.buttonAndHandler(u'Verify')
  def verify(self, action):
    data, errors = self.extractData()
    current_user = getToolByName(self.context,'portal_membership').getAuthenticatedMember().getId()
    return 'NYI...'