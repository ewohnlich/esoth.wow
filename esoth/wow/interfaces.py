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
  
class IPetUtility(Interface):
  """ Pet data utility"""
  
class IMountUtility(Interface):
  """ Mount data utility"""
  
specs = SimpleVocabulary(
    [SimpleTerm(value=u'blood-dk', title=_(u'Death Knight (Blood)')),
     SimpleTerm(value=u'frost-dk', title=_(u'Death Knight (Frost/Unholy)')),
     SimpleTerm(value=u'guardian-druid', title=_(u'Druid (Guardian)')),
     SimpleTerm(value=u'feral-druid', title=_(u'Druid (Feral)')),
     SimpleTerm(value=u'balance-druid', title=_(u'Druid (Balance)')),
     SimpleTerm(value=u'restoration-druid', title=_(u'Druid (Restoration)')),
     SimpleTerm(value=u'hunter', title=_(u'Hunter')),
     SimpleTerm(value=u'mage', title=_(u'Mage')),
     SimpleTerm(value=u'mistweaver-monk', title=_(u'Monk (Mistweaver)')),
     SimpleTerm(value=u'brewmaster-monk', title=_(u'Monk (Brewmaster)')),
     SimpleTerm(value=u'windwalker-monk', title=_(u'Monk (Windwalker)')),
     SimpleTerm(value=u'holy-paladin', title=_(u'Paladin (Holy)')),
     SimpleTerm(value=u'protection-paladin', title=_(u'Paladin (Protection)')),
     SimpleTerm(value=u'retribution-paladin', title=_(u'Paladin (Retribution)')),
     SimpleTerm(value=u'holy-priest', title=_(u'Priest (Holy/Discipline)')),
     SimpleTerm(value=u'shadow-priest', title=_(u'Priest (Shadow)')),
     SimpleTerm(value=u'rogue', title=_(u'Rogue')),
     SimpleTerm(value=u'elemental-shaman', title=_(u'Shaman (Elemental)')),
     SimpleTerm(value=u'enhancement-shaman', title=_(u'Shaman (Enhancement)')),
     SimpleTerm(value=u'restoration-shaman', title=_(u'Shaman (Restoration)')),
     SimpleTerm(value=u'warlock', title=_(u'Warlock')),
     SimpleTerm(value=u'arms-warrior', title=_(u'Warrior (Arms)')),
     SimpleTerm(value=u'fury-warrior', title=_(u'Warrior (Fury)')),
     SimpleTerm(value=u'protection-warrior', title=_(u'Warrior (Protection)')),]
    )

realms = []
try:
  realms = json.load(urlopen('http://us.battle.net/api/wow/realm/status'))['realms']
except:
  try:
    realms = json.load(urlopen('http://www.esoth.com/proxyw?u=http://us.battle.net/api/wow/realm/status'))['realms']
  except:
    pass
servers = SimpleVocabulary([SimpleTerm(value=r['slug'], title=_('%s (US)' % r['name'])) for r in realms])

class ICharDisplay(form.Schema):
  title = schema.TextLine(title=_(u"Display name"))
  description = schema.Text(title=_(u"Description"))
  groups = schema.Set(title=_(u"Group(s)"),
                             value_type=schema.TextLine(required=False),
                             required=False,)
  guild = schema.TextLine(title=_(u"Guild"),required=False)
  server = schema.TextLine(title=_(u"Server"),required=False)

class IGearSchema(form.Schema):
  name = schema.TextLine(title=_(u"Name"),required=False)
  source = schema.TextLine(title=_(u"Source"),required=False)
  itemIds = schema.List(title=_(u"Item IDs"),
                  value_type=schema.TextLine(),required=False,
            )
  ilvls = schema.List(title=_(u"Ilvls"),
                  value_type=schema.TextLine(),required=False,
            )
  klass = schema.TextLine(title=_(u"Class Restriction"),required=False)
  slot = schema.TextLine(title=_(u"Slot"),required=False)
  armorClass = schema.TextLine(title=_(u"Armor Class"),required=False)
  icon = schema.TextLine(title=_(u"Icon"),required=False)
  agility = schema.Bool(title=_(u"Agi"),required=False)
  strength = schema.Bool(title=_(u"Strength"),required=False)
  intellect = schema.Bool(title=_(u"Intellect"),required=False)
  spirit = schema.Bool(title=_(u"Spirit"),required=False)
  dodge = schema.Bool(title=_(u"Dodge"),required=False)
  parry = schema.Bool(title=_(u"Parry"),required=False)
  dps_flag = schema.Bool(title=_(u"DPS explicit"),required=False)
  healer_flag = schema.Bool(title=_(u"Healer explicit"),required=False)
  weaponType = schema.TextLine(title=_(u"Weapon Type"),required=False)

class IMountResourceSchema(Interface):
  """ Mount info from armory will actually be stored on each character
      This is just external information """
  spellId = schema.TextLine(title=_(u"Spell ID"),required=False)
  restriction = schema.TextLine(title=_(u"Class Restriction"),required=False)
  name = schema.TextLine(title=_(u"Name"),required=False)
  icon = schema.TextLine(title=_(u"Icon"),required=False)
  faction = schema.TextLine(title=_(u"Faction"),required=False)
  isGround = schema.Bool(title=_(u"Ground"),required=False)
  isAquatic = schema.Bool(title=_(u"Aquatic"),required=False)
  isFlying = schema.Bool(title=_(u"Flying"),required=False)
  isJumping = schema.Bool(title=_(u"Jumping"),required=False)
  obtainable = schema.TextLine(title=_(u"Obtainable"),required=False)
  location = schema.TextLine(title=_(u"Location"),required=False)
  
class IMountSchema(Interface):
  name = schema.TextLine(title=_(u"Name"),required=False)
  creatureId = schema.TextLine(title=_(u"Creature ID"),required=False)
  itemId = schema.TextLine(title=_(u"Item ID"),required=False)
  spellId = schema.TextLine(title=_(u"Spell ID"),required=False)
  icon = schema.TextLine(title=_(u"Icon"),required=False)
  source = schema.TextLine(title=_(u"Source"),required=False)
  isCollected = schema.Bool(title=_(u"isCollected"),required=False)
  isGround = schema.Bool(title=_(u"isGround"),required=False)
  isFlying = schema.Bool(title=_(u"isFlying"),required=False)
  isAquatic = schema.Bool(title=_(u"isAquatic"),required=False)
  isJumping = schema.Bool(title=_(u"isJumping"),required=False)

class IPetResourceSchema(Interface):
  speciesId = schema.TextLine(title=_(u"Species ID"),required=False)
  health = schema.TextLine(title=_(u"Health"),required=False)
  power = schema.TextLine(title=_(u"Power"),required=False)
  speed = schema.TextLine(title=_(u"Speed"),required=False)
  
class IPetSchema(Interface):
  name = schema.TextLine(title=_(u"Name"),required=False)
  creatureName = schema.TextLine(title=_(u"Creature Name"),required=False)
  spellId = schema.TextLine(title=_(u"Spell ID"),required=False)
  creatureId = schema.TextLine(title=_(u"Creature ID"),required=False)
  speciesId = schema.TextLine(title=_(u"Species ID"),required=False)
  qualityId = schema.TextLine(title=_(u"Quality ID"),required=False)
  icon = schema.TextLine(title=_(u"Icon"),required=False)
  breedId = schema.TextLine(title=_(u"Breed ID"),required=False)
  level = schema.TextLine(title=_(u"Level"),required=False)
  health = schema.TextLine(title=_(u"Health"),required=False)
  power = schema.TextLine(title=_(u"Power"),required=False)
  speed = schema.TextLine(title=_(u"Speed"),required=False)
  canBattle = schema.TextLine(title=_(u"Can Battle?"),required=False)

class IWoWResources(Interface):
  """ """

class IWoWResourcesSchema(form.Schema):
  title = schema.TextLine(title=_(u"Title"))
  form.widget(pets=DataGridFieldFactory)
  pets = schema.List(title=u"Pets",
                     value_type=DictRow(title=u"pet", schema=IPetResourceSchema),
                     required=False,
         )
  form.widget(mounts=DataGridFieldFactory)
  mounts = schema.List(title=u"Mouts",
                     value_type=DictRow(title=u"mount", schema=IMountResourceSchema),
                     required=False,
         )
  form.widget(gear=DataGridFieldFactory)
  gear = schema.List(title=u"Gear",
                     value_type=DictRow(title=u"mount", schema=IGearSchema),
                     required=False,
         )

class ISpecSchema(Interface):
  name = schema.TextLine(title=_(u"Name"))
  icon = schema.TextLine(title=_(u"Icon"))

class ITalentSchema(Interface):
  tier = schema.TextLine(title=_(u"Tier"))
  column = schema.TextLine(title=_(u"Column"))
  id = schema.TextLine(title=_(u"ID"))
  name = schema.TextLine(title=_(u"Name"))
  icon = schema.TextLine(title=_(u"Icon"))

class IProgressionSchema(Interface):
  tier = schema.TextLine(title=_(u"Tier"))
  raid = schema.TextLine(title=_(u"Raid"))
  boss = schema.TextLine(title=_(u"Boss"))
  nkills = schema.TextLine(title=_(u"Normal Kills"))
  hkills = schema.TextLine(title=_(u"Heroic Kills"))

class IGearPath(form.Schema):

  title = schema.TextLine(title=_(u"Character name"))

  server = schema.Choice(title=_(u"Server"),
          vocabulary=servers,
        )
  
  spec = schema.List(
            title=_(u"Specs"),
            description=_(u"Choose one or more specs. The available choices will be a union of all gear associated with those specs. For instance if you just select Restoration Shaman you will not see agi gear"), 
            value_type=schema.Choice(
              vocabulary=specs,
            )
        )
        
  mode(faction='hidden')
  faction = schema.TextLine(
            title=_(u"Faction"),
            required=False,
        )
  mode(slotToBlank1='hidden')
  slotToBlank1 = schema.TextLine(required=False)
  mode(slotToBlank2='hidden')
  slotToBlank2 = schema.TextLine(required=False)
  mode(slotToBlank3='hidden')
  slotToBlank3 = schema.TextLine(required=False)
  mode(slotToBlank3='verifier')
  verifier = schema.TextLine(required=False)

  mode(weapon='hidden')
  weapon = schema.TextLine(
            title=_(u"Weapon"),
            required=False,
        )
  
  mode(offhand='hidden')
  offhand = schema.TextLine(
            title=_(u"Off Hand"),
            required=False,
        )

  mode(head='hidden')
  head = schema.TextLine(
            title=_(u"Head"),
            required=False,
        )

  mode(neck='hidden')
  neck = schema.TextLine(
            title=_(u"Neck"),
            required=False,
        )

  mode(shoulders='hidden')
  shoulders = schema.TextLine(
            title=_(u"Shoulders"),
            required=False,
        )

  mode(back='hidden')
  back = schema.TextLine(
            title=_(u"Back"),
            required=False,
        )

  mode(chest='hidden')
  chest = schema.TextLine(
            title=_(u"Chest"),
            required=False,
        )

  mode(wrists='hidden')
  wrists = schema.TextLine(
            title=_(u"Wrists"),
            required=False,
        )

  mode(hands='hidden')
  hands = schema.TextLine(
            title=_(u"Hands"),
            required=False,
        )

  mode(waist='hidden')
  waist = schema.TextLine(
            title=_(u"Waist"),
            required=False,
        )

  mode(legs='hidden')
  legs = schema.TextLine(
            title=_(u"Legs"),
            required=False,
        )

  mode(feet='hidden')
  feet = schema.TextLine(
            title=_(u"Feet"),
            required=False,
        )

  mode(ring1='hidden')
  ring1 = schema.TextLine(
            title=_(u"Ring (1)"),
            required=False,
        )

  mode(ring2='hidden')
  ring2 = schema.TextLine(
            title=_(u"Ring (2)"),
            required=False,
        )

  mode(trinket1='hidden')
  trinket1 = schema.TextLine(
            title=_(u"Trinket (1)"),
            required=False,
        )

  mode(trinket2='hidden')
  trinket2 = schema.TextLine(
            title=_(u"Trinket (2)"),
            required=False,
        )

  mode(lastupdated='hidden')
  lastupdated = schema.Date(title=_(u"Last updated"),required=False)

  acquiredItems = schema.Set(title=_(u"Acquired"),
                             value_type=schema.TextLine(required=False),
                             required=False,)
  bisItems = schema.Set(title=_(u"BIS"),
                        value_type=schema.TextLine(required=False),
                        required=False,)
  downgradeItems = schema.Set(title=_(u"Downgrade"),
                              value_type=schema.TextLine(required=False),
                              required=False,)
                              
  ### begin old wowchar fields
  groups = schema.List(title=_(u"Groups"),
                       description=_(u"This is used to group a bunch of people together, such as &lt;Something Wicked&gt;'s roster"),
                       value_type=schema.TextLine(required=False),
                       required=False,
           )
           
  mode(race='hidden')
  race = schema.TextLine(required=False)
  
  mode(gender='hidden')
  gender = schema.TextLine(required=False)
  
  mode(averageItemLevel='hidden')
  averageItemLevel = schema.TextLine(required=False)
  
  mode(averageItemLevelEquipped='hidden')
  averageItemLevelEquipped = schema.TextLine(required=False)
  
  mode(mounts='hidden')
  mounts = schema.TextLine(required=False)
  mountDetails = schema.List(title=u"Mount (details)",
                     value_type=DictRow(title=u"mountrow", schema=IMountSchema),
                     required=False
         )
  
  progression = schema.List(title=u"Progression",
                            value_type=DictRow(title=u"progrow", schema=IProgressionSchema),
                            required=False
                )
  
  pets = schema.List(title=u"Pets",
                     value_type=DictRow(title=u"petrow", schema=IPetSchema),
                     required=False
         )
  
  specs = schema.List(title=u"Specs",
                     value_type=DictRow(title=u"specrow", schema=ISpecSchema),
                     required=False
         )
         
  
  mainTalents = schema.List(title=u"Main Talents",
                     value_type=DictRow(title=u"maintalentrow", schema=ITalentSchema),
                     required=False
         )
         
  
  secondTalents = schema.List(title=u"Secondary Talents",
                     value_type=DictRow(title=u"secondtalentrow", schema=ITalentSchema),
                     required=False
         )
  
  mode(level='hidden')
  level = schema.TextLine(required=False)
  
  mode(klass='hidden')
  klass = schema.TextLine(required=False)
  
  mode(titles='hidden')
  titles = schema.TextLine(required=False)
  
  mode(guild='hidden')
  guild = schema.TextLine(required=False)
  
  avatar = NamedImage(title=u"Avatar",required=False)
  
  mode(points='hidden')
  points = schema.Int(required=False)
  
  mode(agility='hidden')
  agility = schema.TextLine(required=False)
  
  mode(strength='hidden')
  strength = schema.TextLine(required=False)
  
  mode(intellect='hidden')
  intellect = schema.TextLine(required=False)
  
  mode(spirit='hidden')
  spirit = schema.TextLine(required=False)
  
  mode(stamina='hidden')
  stamina = schema.TextLine(required=False)
  
  mode(crit='hidden')
  crit = schema.TextLine(required=False)
  
  mode(haste='hidden')
  haste = schema.TextLine(required=False)
  
  mode(mastery='hidden')
  mastery = schema.TextLine(required=False)
  
  mode(hit='hidden')
  hit = schema.TextLine(required=False)
  
  mode(expertise='hidden')
  expertise = schema.TextLine(required=False)