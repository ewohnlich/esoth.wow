from collective.z3cform.datagridfield import DictRow, DataGridFieldFactory
import json
from plone.autoform.directives import mode
from plone.directives import form
from plone.namedfile.field import NamedImage
from urllib import urlopen
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from esoth.wow import _

hellfire = ['Hellfire Assault','Iron Reaver','Kormrok','Hellfire High Council','Kilrogg Deadeye','Gorefiend',
              'Shadow-Lord Iskar','Socrethar the Eternal','Tyrant Velhari','Fel Lord Zakuun','Xhul\'horac',
              'Mannoroth','Archimonde']
loot_sources = SimpleVocabulary([SimpleTerm(value=v, title=_(v)) for v in hellfire]+[
          SimpleTerm(value=u'Legendary', title=_(u'Legendary')),
          SimpleTerm(value=u'Blackrock Foundry', title=_(u'Blackrock Foundry')),
          SimpleTerm(value=u'other', title=_(u'Other')),])

class ICharacter(form.Schema):
  title = schema.TextLine(title=_(u"Name"),required=False)
  guild = schema.TextLine(title=_(u"Guild"),required=False)
  server = schema.TextLine(title=_(u"Server"),required=False)
  region = schema.TextLine(title=_(u"Region"),required=False)
  thumbnail = schema.TextLine(title=_(u"Thumbnail"),required=False)
  gear = schema.Set(title=_(u"Looted Gear"),
                     required=False,
                     value_type=schema.TextLine())
  downgrades = schema.Set(title=_(u"Marked Downgrades"),
                     required=False,
                     value_type=schema.TextLine())
  weapon = schema.Float(title=_(u"Weapon Score"),required=False)
  agility = schema.Float(title=_(u"Agi Score"),required=False)
  strength = schema.Float(title=_(u"Strength Score"),required=False)
  intellect = schema.Float(title=_(u"Intellect Score"),required=False)
  crit = schema.Float(title=_(u"Crit Score"),required=False)
  haste = schema.Float(title=_(u"Haste Score"),required=False)
  mastery = schema.Float(title=_(u"Mastery Score"),required=False)
  multistrike = schema.Float(title=_(u"Multistrike Score"),required=False)
  versatility = schema.Float(title=_(u"Versatility Score"),required=False)

class IGearContext(form.Schema):
  gear_context = schema.TextLine(title=_(u"Context"),required=False)
  ilvl = schema.TextLine(title=_(u"Ilvl"),required=False)
  agility = schema.Int(title=_(u"Agi"),required=False)
  strength = schema.Int(title=_(u"Strength"),required=False)
  intellect = schema.Int(title=_(u"Intellect"),required=False)
  crit = schema.Int(title=_(u"Crit"),required=False)
  haste = schema.Int(title=_(u"Haste"),required=False)
  mastery = schema.Int(title=_(u"Mastery"),required=False)
  multistrike = schema.Int(title=_(u"Multistrike"),required=False)
  versatility = schema.Int(title=_(u"Versatility"),required=False)

class IGearItem(form.Schema):
  title = schema.TextLine(title=_(u"Name"),required=False)
  boss = schema.Choice(title=_(u"Boss or Source"),
                       vocabulary = loot_sources,
                       required=False)
  item_id = schema.TextLine(title=_(u"Item ID"),required=False)
  form.widget(contexts=DataGridFieldFactory)
  contexts = schema.List(
            title=_(u"Available Contexts"),
            value_type=DictRow(title=_(u"section"), schema=IGearContext),
            required=False,
        )
  slot = schema.TextLine(title=_(u"Slot"),required=False)
  armor_class = schema.TextLine(title=_(u"Armor Class"),required=False)
  weapon_type = schema.TextLine(title=_(u"Weapon Type"),required=False)
  icon = schema.TextLine(title=_(u"Icon"),required=False)
  klass = schema.TextLine(title=_(u"Class Restriction"),required=False)

class IGearSlots(form.Schema):
  head = schema.TextLine(title=_(u""),required=False)
  neck = schema.TextLine(title=_(u""),required=False)
  shoulder = schema.TextLine(title=_(u""),required=False)
  back = schema.TextLine(title=_(u""),required=False)
  chest = schema.TextLine(title=_(u""),required=False)
  wrist = schema.TextLine(title=_(u""),required=False)
  hands = schema.TextLine(title=_(u""),required=False)
  waist = schema.TextLine(title=_(u""),required=False)
  legs = schema.TextLine(title=_(u""),required=False)
  feet = schema.TextLine(title=_(u""),required=False)
  finger1 = schema.TextLine(title=_(u""),required=False)
  finger2 = schema.TextLine(title=_(u""),required=False)
  trinket1 = schema.TextLine(title=_(u""),required=False)
  trinket2 = schema.TextLine(title=_(u""),required=False)
  mainHand = schema.TextLine(title=_(u""),required=False)
  offHand = schema.TextLine(title=_(u""),required=False)

slot_alt_name = {'head':'Head',
                 'neck':'Neck',
                 'shoulder':'Shoulder',
                 'back':'Back',
                 'chest':'Chest',
                 'wrist':'Wrist',
                 'hands':'Hands',
                 'waist':'Waist',
                 'legs':'Legs',
                 'feet':'Feet',
                 'finger1':'Ring',
                 'finger2':'Ring',
                 'trinket1':'Trinket',
                 'trinket2':'Trinket',
                 'mainHand':'mainHand',
                 'offHand':'offHand'}