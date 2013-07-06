from five import grok
from plone.dexterity.content import Item
from plone.directives import form
from zope import schema
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from esoth.wow import _
from esoth.wow.content.gear import boss, gear, slot as slot

@grok.provider(IContextSourceBinder)
def choices_weapon(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Weapon']])

@grok.provider(IContextSourceBinder)
def choices_head(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Head']])

@grok.provider(IContextSourceBinder)
def choices_neck(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Neck']])

@grok.provider(IContextSourceBinder)
def choices_shoulders(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Shoulders']])

@grok.provider(IContextSourceBinder)
def choices_back(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Back']])

@grok.provider(IContextSourceBinder)
def choices_chest(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Chest']])

@grok.provider(IContextSourceBinder)
def choices_wrists(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Wrists']])

@grok.provider(IContextSourceBinder)
def choices_hands(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Hands']])

@grok.provider(IContextSourceBinder)
def choices_waist(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Waist']])

@grok.provider(IContextSourceBinder)
def choices_legs(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Legs']])

@grok.provider(IContextSourceBinder)
def choices_feet(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Feet']])

@grok.provider(IContextSourceBinder)
def choices_ring(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Ring']])

@grok.provider(IContextSourceBinder)
def choices_trinket(context): return SimpleVocabulary([SimpleTerm(value=_(t), title=_(t)) for t in slot['Trinket']])

class IGearPath(form.Schema):

  title = schema.TextLine(title=_(u"Title"))

  weapon = schema.Choice(
            title=_(u"Weapon"),
            source=choices_weapon,
            required=False,
        )

  head = schema.Choice(
            title=_(u"Head"),
            source=choices_head,
            required=False,
        )

  neck = schema.Choice(
            title=_(u"Neck"),
            source=choices_neck,
            required=False,
        )

  shoulders = schema.Choice(
            title=_(u"Shoulders"),
            source=choices_shoulders,
            required=False,
        )

  back = schema.Choice(
            title=_(u"Back"),
            source=choices_back,
            required=False,
        )

  chest = schema.Choice(
            title=_(u"Chest"),
            source=choices_chest,
            required=False,
        )

  wrists = schema.Choice(
            title=_(u"Wrists"),
            source=choices_wrists,
            required=False,
        )

  hands = schema.Choice(
            title=_(u"Hands"),
            source=choices_hands,
            required=False,
        )

  waist = schema.Choice(
            title=_(u"Waist"),
            source=choices_waist,
            required=False,
        )

  legs = schema.Choice(
            title=_(u"Legs"),
            source=choices_legs,
            required=False,
        )

  feet = schema.Choice(
            title=_(u"Feet"),
            source=choices_feet,
            required=False,
        )

  ring1 = schema.Choice(
            title=_(u"Ring (1)"),
            source=choices_ring,
            required=False,
        )

  ring2 = schema.Choice(
            title=_(u"Ring (2)"),
            source=choices_ring,
            required=False,
        )

  trinket1 = schema.Choice(
            title=_(u"Trinket (1)"),
            source=choices_trinket,
            required=False,
        )

  trinket2 = schema.Choice(
            title=_(u"Trinket (2)"),
            source=choices_trinket,
            required=False,
        )

  acquiredItems = schema.Set(title=_(u"Acquired"),
                             value_type=schema.TextLine(),
                             required=False,)
  bisItems = schema.Set(title=_(u"BIS"),
                        value_type=schema.TextLine(),
                        required=False,)
  downgradeItems = schema.Set(title=_(u"Downgrade"),
                              value_type=schema.TextLine(),
                              required=False,)

class GearPath(Item):
    """ """
    implements(IGearPath)
    meta_type = 'GearPath'

    def gearMap(self):
      _map = {}

      def isequipped(i,s):
        s=s.lower()
        if s in ['trinket','ring']:
          return (getattr(self,s+'1') and i in getattr(self,s+'1')) or (getattr(self,s+'2') and i in getattr(self,s+'2'))
        return i == getattr(self,s)

      for k in slot.keys():
        count = len(slot[k])
        itms = []
        for v in slot[k]:
          itm = {'name':v,
                 'id':gear[v]['id'],
                 'boss':gear[v]['boss'],
                 'bis':self.bisItems and v in self.bisItems,
                 'acquired':self.acquiredItems and v in self.acquiredItems,
                 'downgrade':self.downgradeItems and v in self.downgradeItems,
                 'equipped':isequipped(v,k)}
          itms.append(itm)
        _map[k.lower()] = {'count':count+2,'itms':itms}
      return _map

    def bossNeeds(self):
      # name, slot
      neededSlots = []
      bossItems = {}

      ignored_items = set(list(self.acquiredItems or [])+list(self.downgradeItems or [])+[self.trinket1,self.trinket2,self.ring1,self.ring2])

      bisItems = self.bisItems or []
      for _k in slot.keys():
        k = _k.lower()
        if k in ['trinket','ring']:
          eq1 = getattr(self,k+'1')
          eq2 = getattr(self,k+'2')
          if eq1 not in bisItems or eq2 not in bisItems:
            neededSlots.append(_k)
        else:
          eq = getattr(self,k)
          if eq not in bisItems:
            neededSlots.append(_k)
      for b in boss.keys():
        bossItems[b] = []
        for s in boss[b].keys(): # check each slot
          if s in neededSlots:
            bossItems[b] += [{'slot':s,'name':i,'id':gear[i]['id']} for i in boss[b][s] if i not in ignored_items ]
      return bossItems
    
    def bossOrder(self):
      return ['Jin\'rokh','Horridon','Zandalari Council','Tortos','Megaera','Ji-kun','Durumu','Primordius','Dark Animus','Iron Qon','Twin Consorts','Lei Shen','Ra-den','Legendary']