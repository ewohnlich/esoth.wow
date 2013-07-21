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
      slots = ['Head','Neck','Shoulders','Back','Chest','Wrists','Hands','Waist','Legs','Feet','Ring1','Ring2','Trinket1','Trinket2']
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
    current_user = getToolByName(self.context,'portal_membership').getAuthenticatedMember()
    user_id = current_user.getId()
    
    if user_id != self.context.verifier:
      IStatusMessage(self.request).addStatusMessage(_(u"Your verifying character is invalid"),"error")
      self.request.response.redirect(self.context.absolute_url()+'/@@character-verify')
    
    base_url = 'http://us.battle.net/api/wow/character/%s/%s?fields=items'
    url = base_url % (self.context.server,self.context.title)
    try:
      data = json.load(urlopen(url))
    except ValueError:
      data = json.load(urlopen('http://www.esoth.com/proxyw?u='+url))
    gear = data['items']
    blankslots = (self.context.slotToBlank1,self.context.slotToBlank2,self.context.slotToBlank3)
    
    check_slots = ['Head','Neck','Shoulders','Back','Chest','Wrists','Hands','Waist','Legs','Feet','Ring1','Ring2','Trinket1','Trinket2']
    for sl in check_slots:
      if sl in blankslots:
        if gear.get(sl.lower().replace('ring','finger').replace('shoulders','shoulder').replace('wrists','wrist')):
          IStatusMessage(self.request).addStatusMessage(_(u"Validation failed - check you only unequipped these slots"),"error")
          self.request.response.redirect(self.context.absolute_url()+'/@@character-verify')
          return
      else:
        if not gear.get(sl.lower().replace('ring','finger').replace('shoulders','shoulder').replace('wrists','wrist')):
          IStatusMessage(self.request).addStatusMessage(_(u"Validation failed - check you only unequipped these slots"),"error")
          self.request.response.redirect(self.context.absolute_url()+'/@@character-verify')
          return
    # success
    self.context.manage_setLocalRoles(user_id, ['Editor'])
    self.slotToBlank1 = ''
    self.slotToBlank2 = ''
    self.slotToBlank3 = ''
    IStatusMessage(self.request).addStatusMessage(_(u"You can now edit this character"),"info")
    self.request.response.redirect(self.context.absolute_url()+'/@@gearpath-view')