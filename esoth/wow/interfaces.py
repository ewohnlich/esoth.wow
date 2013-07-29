from collective.z3cform.datagridfield import DictRow
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

try:
  realms = json.load(urlopen('http://us.battle.net/api/wow/realm/status'))['realms']
except:
  realms = json.load(urlopen('http://www.esoth.com/proxyw?u=http://us.battle.net/api/wow/realm/status'))['realms']
servers = SimpleVocabulary([SimpleTerm(value=r['slug'], title=_('%s (US)' % r['name'])) for r in realms])

class ICharDisplay(form.Schema):
  title = schema.TextLine(title=_(u"Display name"))
  description = schema.Text(title=_(u"Description"))
  groups = schema.Set(title=_(u"Group(s)"),
                             value_type=schema.TextLine(required=False),
                             required=False,)
  guild = schema.TextLine(title=_(u"Guild"),required=False)
  server = schema.TextLine(title=_(u"Server"),required=False)
  
class IMountSchema(Interface):
  name = schema.TextLine(title=_(u"Name"))
  creatureId = schema.TextLine(title=_(u"Creature ID"))
  itemId = schema.TextLine(title=_(u"Item ID"))
  icon = schema.TextLine(title=_(u"Icon"))
  source = schema.TextLine(title=_(u"Source"))
  isCollected = schema.Bool(title=_(u"isCollected"))
  isGround = schema.Bool(title=_(u"isGround"))
  isFlying = schema.Bool(title=_(u"isFlying"))
  isAquatic = schema.Bool(title=_(u"isAquatic"))
  isJumping = schema.Bool(title=_(u"isJumping"))

class IPetSchema(Interface):
  name = schema.TextLine(title=_(u"Name"))
  creatureName = schema.TextLine(title=_(u"Creature Name"))
  spellId = schema.TextLine(title=_(u"Spell ID"))
  creatureId = schema.TextLine(title=_(u"Creature ID"))
  speciesId = schema.TextLine(title=_(u"Species ID"))
  qualityId = schema.TextLine(title=_(u"Quality ID"))
  icon = schema.TextLine(title=_(u"Icon"))
  breedId = schema.TextLine(title=_(u"Breed ID"))
  level = schema.TextLine(title=_(u"Level"))
  health = schema.TextLine(title=_(u"Health"))
  power = schema.TextLine(title=_(u"Power"))
  speed = schema.TextLine(title=_(u"Speed"))
  canBattle = schema.TextLine(title=_(u"Can Battle?"))

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