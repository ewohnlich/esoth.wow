from five import grok
from plone.dexterity.content import Item
from plone.directives import form
from zope import schema
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from esoth.wow import _
from esoth.wow.content.gear import getGear

 
specs = SimpleVocabulary(
    [SimpleTerm(value=u'hunter', title=_(u'Hunter')),
     SimpleTerm(value=u'elemental-shaman', title=_(u'Elemental Shaman')),]
    )

class IGearPath(form.Schema):

  title = schema.TextLine(title=_(u"Title"))
  
  spec = schema.Choice(
            title=_(u"Spec"),
            vocabulary=specs,
        )

  weapon = schema.TextLine(
            title=_(u"Weapon"),
            required=False,
        )
  
  offhand = schema.TextLine(
            title=_(u"Off Hand"),
            required=False,
        )

  head = schema.TextLine(
            title=_(u"Head"),
            required=False,
        )

  neck = schema.TextLine(
            title=_(u"Neck"),
            required=False,
        )

  shoulders = schema.TextLine(
            title=_(u"Shoulders"),
            required=False,
        )

  back = schema.TextLine(
            title=_(u"Back"),
            required=False,
        )

  chest = schema.TextLine(
            title=_(u"Chest"),
            required=False,
        )

  wrists = schema.TextLine(
            title=_(u"Wrists"),
            required=False,
        )

  hands = schema.TextLine(
            title=_(u"Hands"),
            required=False,
        )

  waist = schema.TextLine(
            title=_(u"Waist"),
            required=False,
        )

  legs = schema.TextLine(
            title=_(u"Legs"),
            required=False,
        )

  feet = schema.TextLine(
            title=_(u"Feet"),
            required=False,
        )

  ring1 = schema.TextLine(
            title=_(u"Ring (1)"),
            required=False,
        )

  ring2 = schema.TextLine(
            title=_(u"Ring (2)"),
            required=False,
        )

  trinket1 = schema.TextLine(
            title=_(u"Trinket (1)"),
            required=False,
        )

  trinket2 = schema.TextLine(
            title=_(u"Trinket (2)"),
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
      boss,slot,gear = getGear(self.spec)
      _map = {}

      worn_slots = ['Weapon','Off Hand','Head','Neck','Shoulders','Back','Chest','Wrists','Hands','Waist','Legs','Feet','Ring1','Ring2','Trinket1','Trinket2']
      for k in worn_slots:
        item_type = k.replace('1','').replace('2','')
        count = len(slot.get(item_type,[]))
        itms = []
        for v in slot.get(item_type,[]):
          itm = {'name':v,
                 'id':gear[v]['id'],
                 'boss':gear[v]['boss'],
                 'bis':self.bisItems and v in self.bisItems,
                 'acquired':self.acquiredItems and v in self.acquiredItems,
                 'downgrade':self.downgradeItems and v in self.downgradeItems,
                 'equipped':v == getattr(self,k.lower().replace(' ',''))}
          itms.append(itm)
        _map[k.lower()] = {'count':count+2,'itms':itms}
      return _map

    def bossNeeds(self):
      boss,slot,gear = getGear(self.spec)
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