import logging
import plone.api
from plone.dexterity.content import Item
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.interface import implements, Interface
from zope.schema import getFieldsInOrder

from esoth.wow import _
from esoth.wow.config import API_KEY
from esoth.wow.interfaces import IGearSlots
from esoth.wow.tools import get_character

logger = logging.getLogger('esoth.wow')

class Character(Item):
  """ """

  def secondary(self):
    """ Find which attribute to increase by gem value """
    statmap = {}
    stats = ('crit','haste','mastery','multistrike','versatility')
    for stat in stats:
      statmap[getattr(self,stat)]=stat
    return statmap[max([getattr(self,s) for s in stats])]

  def getIcon(self,dummy=True):
    if self.thumbnail:
      return '@@get_icon?tag=%s&avatar=True' % self.thumbnail
    else:
      return '%s/++resource++esoth.wow/wowchar.png' % plone.api.portal.get().absolute_url()

  def update_character(self):
    if self.region and self.server and self.title:
      character = get_character(self.region,self.server,self.title)
      self.thumbnail = character['thumbnail']

      if not self.gear:
        self.gear = set()
      for slot,dummy in getFieldsInOrder(IGearSlots):
        if slot in character['items']: # offhand might not exist
          gear_item = '%d_%s' % (character['items'][slot]['id'], character['items'][slot]['context'])
          if 562 in character['items'][slot]['bonusLists']:
            gear_item += ' (w)'
          if 565 in character['items'][slot]['bonusLists']:
            gear_item += ' (s)'
          self.gear.add(gear_item)
      self.reindexObject()

  def get_gear(self):
    catalog = getToolByName(self, 'portal_catalog')
    gear_set = []

    if not self.gear:
      self.update_character()

    for gearstring in self.gear:
      item_id,gear_context = gearstring.split('_')
      brains = catalog(item_id=item_id)
      if brains:
        brain = brains[0]
        for gc in brain.contexts:
          if (gc['gear_context'] == gear_context) or (not gc['gear_context'] and gear_context == 'vendor'): # legendary
            gear_item = {'title':brain.Title,
                         'slot':brain.slot,
                         'agility':gc['agility'],
                         'strength':gc['strength'],
                         'intellect':gc['intellect'],
                         'crit':gc['crit'],
                         'haste':gc['haste'],
                         'mastery':gc['mastery'],
                         'multistrike':gc['multistrike'],
                         'versatility':gc['versatility'],}
            gear_item['score'] = self.get_score(gear_item)
            gear_set.append(gear_item)
            continue
    return gear_set

  def get_score(self,gear_item):
    stats = ('agility','strength','intellect','crit','haste','mastery','multistrike','versatility')
    return sum([getattr(self,stat)*gear_item[stat] for stat in stats if getattr(self,stat) and gear_item[stat]])

  def get_scores(self):
    slots = {}
    for gear in self.get_gear():
      if gear['slot'] not in slots:
        slots[gear['slot']] = []
      slots[gear['slot']].append(gear['score'])
    return slots