from five import grok
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from zope.schema import getFieldsInOrder

from esoth.wow import _
from esoth.wow.config import GEM_VALUE
from esoth.wow.interfaces import ICharacter, IGearSlots, slot_alt_name
from esoth.wow.tools import context_name, get_character

grok.templatedir('.')

class CharacterView(grok.View):
  grok.context(ICharacter)
  grok.name('view')
  grok.template('character')

  def raid(self):
    catalog = getToolByName(self.context,'portal_catalog')
    bosses = ['Hellfire Assault','Iron Reaver','Kormrok','Hellfire High Council','Kilrogg Deadeye','Gorefiend',
              'Shadow-Lord Iskar','Socrethar the Eternal','Tyrant Velhari','Fel Lord Zakuun','Xhul\'horac',
              'Mannoroth','Archimonde','Legendary','Blackrock Foundry','Other']
    scores = self.context.get_scores() # get the scores of all looted gear

    for boss in bosses:
      gear = []
      for gear_item in catalog(boss=boss):
        for context in gear_item.contexts:
          gear.extend(self.get_gear_from_context(context,gear_item,scores))
      yield {'boss':boss,'gear':gear}

  def get_status(self, id, slot, gear_item, score, scores):
    scores = scores.copy()
    gear_string = '%s_%s' % (id,gear_item['gear_context'])
    if gear_string in (self.context.gear or []):
      return 'looted'
    else:
      if scores[slot]:
        if slot in ('Ring','Trinket'):
          scores[slot].remove(max(scores[slot]))
        if scores[slot]:
          if score < max(scores[slot]):
            return 'downgrade'
    return 'upgrade'

  def resource_base_url(self):
    #return 'http://us.media.blizzard.com'
    return 'http://www.esoth.com/proxyi?u=http://us.media.blizzard.com'

  def get_gear_from_context(self, context, gear_item, scores):
    gear = []
    score = self.context.get_score(context)
    if not context['gear_context']:
      context['gear_context'] = ''
    context['gear_context_name'] = context_name(context['gear_context'])
    # item is our context information (stats) for the gear
    score_diff = scores[gear_item.slot] and score-max(scores[gear_item.slot]) or score
    gear.append({'score':'%.2f' % score,
                 'score_diff':score_diff > 0 and '+%.2f' % score_diff or '%.2f' % score_diff,
                 'item':context,
                 'icon':gear_item.getIcon,
                 'id':gear_item.item_id,
                 'status':self.get_status(gear_item.item_id,gear_item.slot,context,score,scores),
                 'name':gear_item.Title})

    # add a socket to our regular or warforged gear
    # the value will increase by GEM_VALUE * best secondary stat
    if context['gear_context'] in ('raid-normal','raid-heroic','raid-mythic'):
      context=context.copy()
      context['gear_context'] = context['gear_context'] + ' (s)'
      context['gear_context_name'] = context_name(context['gear_context'])
      context[self.context.secondary()] += GEM_VALUE
      score = self.context.get_score(context)
      score_diff = scores[gear_item.slot] and score-max(scores[gear_item.slot]) or score
      gear.append({'score':'%.2f' % score,
              'score_diff':score_diff > 0 and '+%.2f' % score_diff or '%.2f' % score_diff,
              'item':context,
              'icon':gear_item.getIcon,
              'id':gear_item.item_id,
              'status':self.get_status(gear_item.item_id,gear_item.slot,context,score,scores),
              'name':gear_item.Title})
    return gear

class CharacterUpdate(grok.View):
  grok.context(ICharacter)
  grok.name('update')

  def render(self):
    character = get_character(self.context.region,self.context.server,self.context.title)
    self.context.thumbnail = character['thumbnail']

    if not self.context.gear:
      self.context.gear = set()
    for slot,dummy in getFieldsInOrder(IGearSlots):
      if slot in character['items']: # offhand might not exist
        gear_item = '%d_%s' % (character['items'][slot]['id'], character['items'][slot]['context'])
        if 562 in character['items'][slot]['bonusLists']:
          gear_item += ' (w)'
        if 565 in character['items'][slot]['bonusLists']:
          gear_item += ' (s)'
        self.context.gear.add(gear_item)
    self.context.reindexObject()

    IStatusMessage(self.request).addStatusMessage(_(u"Character updated"),"info")
    self.request.response.redirect(self.context.absolute_url())

class SlotsView(CharacterView):
  grok.context(ICharacter)
  grok.name('slots')
  grok.template('slots')

  def raid(self):
    catalog = getToolByName(self.context,'portal_catalog')
    scores = self.context.get_scores() # get the scores of all looted gear

    for slot,dummy in getFieldsInOrder(IGearSlots):
      gear = []
      for gear_item in catalog(slot=slot_alt_name[slot]):
        for context in gear_item.contexts:
          gear.extend(self.get_gear_from_context(context,gear_item,scores))
      yield {'slot':slot,'gear':gear}