from AccessControl import ClassSecurityInfo
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from datetime import datetime, timedelta
from five import grok
from plone.dexterity.content import Item
from plone.directives import form, dexterity
from plone.autoform.directives import mode
from plone.namedfile.field import NamedImage
from plone.namedfile.file import NamedImage as NamedImageFile
from z3c.form import field
from zope import schema
from zope.interface import implements, Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from esoth.wow import _
from esoth.wow.content.gear import getGear
from esoth.wow.pets import breedmap

 
specs = SimpleVocabulary(
    [SimpleTerm(value=u'hunter', title=_(u'Hunter')),
     SimpleTerm(value=u'holy-priest', title=_(u'Holy/Discipline Priest')),
     SimpleTerm(value=u'shadow-priest', title=_(u'Shadow Priest')),
     SimpleTerm(value=u'rogue', title=_(u'Rogue (NYI)')),
     SimpleTerm(value=u'elemental-shaman', title=_(u'Elemental Shaman')),]
    )

from urllib import urlopen
import json
try:
  realms = json.load(urlopen('http://us.battle.net/api/wow/realm/status'))['realms']
except:
  realms = json.load(urlopen('http://www.esoth.com/proxyw?u=http://us.battle.net/api/wow/realm/status'))['realms']
servers = SimpleVocabulary([SimpleTerm(value=r['slug'], title=_('%s (US)' % r['name'])) for r in realms])

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
  form.fieldset(u"pets", label="Pet Info", fields=['pets'], layout='concise')

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
                       description=_(u"This is used to group a bunch of people together, such as <Something Wicked>'s roster"),
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
  
  mode(progression='hidden')
  progression = schema.List(title=u"Progression",
                            value_type=DictRow(title=u"progrow", schema=IProgressionSchema),
                            required=False
                )
  
  mode(pets='hidden')
  pets = schema.List(title=u"Pets",
                     value_type=DictRow(title=u"petrow", schema=IPetSchema),
                     required=False
         )
  
  mode(specs='hidden')
  specs = schema.List(title=u"Specs",
                     value_type=DictRow(title=u"specrow", schema=ISpecSchema),
                     required=False
         )
         
  
  mode(mainTalents='hidden')
  mainTalents = schema.List(title=u"Main Talents",
                     value_type=DictRow(title=u"maintalentrow", schema=ITalentSchema),
                     required=False
         )
         
  
  mode(secondTalents='hidden')
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
  
  mode(avatar='hidden')
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

class GearPath(Item):
    """ """
    implements(IGearPath)
    meta_type = 'GearPath'
    security = ClassSecurityInfo()
    
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
        _map[k.lower().replace(' ','')] = {'count':count+2,'itms':itms}
      return _map

    def bossNeeds(self):
      boss,slot,gear = getGear(self.spec)
      heroicIlvls = set([535,541])
      normalIlvls = set([522,528])
      # name, slot
      neededSlots = []
      bossItems = {}

      ignored_items = set(list(self.acquiredItems or [])+list(self.downgradeItems or [])+[self.trinket1,self.trinket2,self.ring1,self.ring2])

      bisItems = self.bisItems or []
      for _k in slot.keys():
        k = _k.lower().replace(' ','')
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
            def klass(val):
              try:
                ilvl = int(i.split('(')[-1].replace(')',''))
              except ValueError:
                ilvl = ''
              return ilvl in heroicIlvls and 'heroicItem' or ilvl in normalIlvls and 'normalItem'
            bossItems[b] += [{'slot':s,'name':i,'id':gear[i]['id'],'class':klass(i)} for i in boss[b][s] if i not in ignored_items ]
      return bossItems
    
    def bossOrder(self):
      return ['Jin\'rokh','Horridon','Zandalari Council','Tortos','Megaera','Ji-kun','Durumu','Primordius','Dark Animus','Iron Qon','Twin Consorts','Lei Shen','Ra-den','Shared - Throne of Thunder','Legendary']

       
    def updateData(self):
      base_image_url = 'http://us.battle.net/static-render/us/'
      url = 'http://us.battle.net/api/wow/character/%s/%s?fields=guild,talents,stats,items,reputation,professions,appearance,companions,mounts,pets,achievements,progression,titles' % (self.server,self.title.lower())
      equipped = set([])
      try:
        data = json.load(urlopen(url))
      except:
        url = 'http://www.esoth.com/proxyw?u='+url
        data = json.load(urlopen(url))
      gear = data['items']
      
      for k,v in gear.items():
        if isinstance(v,dict):
          name = v['name']
          ilvl = v['itemLevel']
          try:
            iupgrade = v['tooltipParams']['upgrade']['itemLevelIncrement']
          except KeyError:
            iupgrade = 0
          equipped.add('%s (%d)' % (name,ilvl-iupgrade))
      _acquired = self.acquiredItems or set([])
      self.acquiredItems = _acquired.union(equipped)

      server = self.server
      charname = self.Title().lower()

      # general
      self.lastupdated = datetime.now()
      try:
        self.level=data['level']
      except:
        return
      racemap = {'1':'Human','5':'Undead','11':'Draenei','7':'Gnome','8':'Troll','4':'Night Elf','2':'Orc','3':'Dwarf','10':'Blood Elf','22':'Worgen','6':'Tauren','9':'Goblin','25':'Pandaren','26':'Pandaren'}
      self.race = racemap[str(data['race'])]
      self.klass = ['none','Warrior','Paladin','Hunter','Rogue','Priest','Death Knight','Shaman','Mage','Warlock','Monk','Druid'][data['class']]
      self.gender = data['gender'] and 'Female' or 'Male'
      try:
        img = urlopen(base_image_url+data['thumbnail']).read()
      except:
        img = urlopen('http://www.esoth.com/proxyi?u='+base_image_url+data['thumbnail']).read()
      self.avatar = NamedImageFile(img,filename=data['thumbnail'])
      self.points = data['achievementPoints']
      
      # ilvl
      _items = data['items']
      self.averageItemLevel = _items['averageItemLevel']
      self.averageItemLevelEquipped = _items['averageItemLevelEquipped']

      # talents
      talents = data['talents']
      specs = []
      for talentRoot in talents:
        _talents = []
        for talent in talentRoot.get('talents',[]):
          if talent:
            _talent = {}
            _talent['tier'] = str(talent['tier'])
            _talent['column'] = str(talent['column'])
            _talent['id'] = str(talent['spell']['id'])
            _talent['name'] = talent['spell']['name']
            _talent['icon'] = talent['spell']['icon']
            _talents.append(_talent)
        _talents.sort(lambda x,y: cmp(int(x['tier']),int(y['tier'])))
        _spec = {}
        if talentRoot.get('spec'):
          _spec['name'] = talentRoot['spec']['name']
          _spec['icon'] = talentRoot['spec']['icon']
        if talentRoot.get('selected'):
          self.mainTalents = _talents
          specs.insert(0,_spec)
        else:
          self.secondTalents =  _talents
          specs.append(_spec)
      self.specs = specs

      if data.get('guild'):
        self.guild = data['guild']['name']

      # stats
      self.agility = data['stats']['agi']
      self.strength = data['stats']['str']
      self.intellect = data['stats']['int']
      self.spirit = data['stats']['spr']
      self.stamina = data['stats']['sta']
      self.crit = data['stats']['critRating']
      self.haste = data['stats']['hasteRating']
      self.mastery = data['stats']['masteryRating']
      self.hit = data['stats']['hitRating']

      # progression
      tiermap = ['Blackwing Descent',
                 'The Bastion of Twilight',
                 'Throne of the Four Winds',
                 'Firelands',
                 'Dragon Soul',
                 "Mogu'shan Vaults",
                 'Heart of Fear',
                 'Terrace of Endless Spring',
                 'Throne of Thunder']
      raids = data['progression']['raids']
      progression = []
      for raid in raids:
        for boss in raid['bosses']:
          if raid['name'] in tiermap:
            if boss['name'] not in [b['boss'] for b in progression] or boss['name'] == 'Ragnaros':
              # Ragnaros is broken and lists heroic kills independently
              progression.append({'tier':str(tiermap.index(raid['name'])),
                                  'raid':raid['name'],
                                  'boss':boss['name'],
                                  'nkills':str(boss.get('normalKills',0)),
                                  'hkills':str(boss.get('heroicKills',0))})
      progression.sort(lambda x,y: cmp(x['tier'],y['tier']))
      self.progression = progression

      # companions
      pets = data['pets']
      total = pets['numCollected']
      _pets = []
      for pet in pets['collected']:
        _pets.append({'name':pet['name'],
                      'creatureName':pet['creatureName'],
                      'spellId':str(pet['spellId']),
                      'creatureId':str(pet['creatureId']),
                      'speciesId':str(pet['stats']['speciesId']),
                      'qualityId':str(pet['stats']['petQualityId']),
                      'icon':pet['icon'],
                      'breedId':str(pet['stats']['breedId']),
                      'level':str(pet['stats']['level']),
                      'health':str(pet['stats']['health']),
                      'power':str(pet['stats']['power']),
                      'speed':str(pet['stats']['speed']),
                      'canBattle':pet['canBattle'] and 'True' or 'False'} )
      self.pets = _pets

      # mounts
      self.mounts = data['mounts']['numCollected']

      # titles
      self.titles = len(data['titles'])

      self.reindexObject()

    def progressionDisplay(self):
      prog = self.progression

      # holy shit data structure
      tiers = {}
      raids = {}
      bosses = {}
      # tier key: 0-2=Tier 11, 3=Tier 12, 4=Tier 13, 5-7=Tier 14, 8=Tier 15
      tierkey = ['Tier 11','Tier 11','Tier 11','Tier 12','Tier 13','Tier 14','Tier 14','Tier 14','Tier 15']
      # fix for Ragnaros bug
      ragn = {}
      ragh = {}
      for boss in prog:
        # update tiers
        tierk = tierkey[int(boss['tier'])]
        if tierk not in tiers:
          tiers[tierk]=[ boss['raid'] ]
        elif boss['raid'] not in tiers[tierk]:
          tiers[tierk].insert(0, boss['raid'] )
        # update raids
        if boss['raid'] not in raids.keys():
          raids[ boss['raid'] ] = [ boss['boss'] ]
        elif boss['boss'] not in raids[ boss['raid'] ]:
          raids[ boss['raid'] ].append(boss['boss'])
        # bosses
        if boss['boss'] in bosses.keys(): # only needed for stupid Ragnaros bug
          if int(bosses[boss['boss']]['nkills'])==0:
            bosses[boss['boss']]['nkills']=boss['nkills']
          if int(bosses[boss['boss']]['hkills'])==0:
            bosses[boss['boss']]['hkills']=boss['hkills']
        else:
          bosses[boss['boss']]={'nkills':boss['nkills'],'hkills':boss['hkills']}

      # build a dict of raids connected to boss data
      _raids = {}
      for raid in raids.keys():
        _raids[raid] = [{'name':b,'nkills':bosses[b]['nkills'],'hkills':bosses[b]['hkills']} for b in raids[raid]]

      # tie the raid dict into a tier dict
      data = []
      for tier in tiers.keys():
        data.append( {'tier':tier, 'raids':[{'raid':r,'bosses':_raids[r]} for r in tiers[tier] ]} )
      data.sort(lambda x,y: cmp(y['tier'],x['tier'])) # sort by newest raid at top
      return data
      
    def serverTitle(self):
      return servers.getTerm(self.server).title

    security.declarePublic('numcompanions')
    def numcompanions(self):
      if self.pets:
        names = [p.get('creatureId') for p in self.pets]
        uniques = {}.fromkeys(names).keys()
        return len( uniques )

    def predictPet(self, petdata, p):
      leveldiff = 25-int(p['level'])
      rarity = int(p['qualityId'])*.1+1
      base = petdata.get( p['speciesId'] )
      if base:
        p['maxH'] = int( round( 25 * (base['health'] + breedmap[p['breedId']]['health']) * rarity * 5 + 100 ))
        p['maxS'] = int( round( 25 * (base['speed'] + breedmap[p['breedId']]['speed']) * rarity ))
        p['maxP'] = int( round( 25 * (base['power'] + breedmap[p['breedId']]['power']) * rarity ))

    security.declarePublic('petData')
    def petData(self):
      data = {'numUnique':0,
              'numTotal':0,
              'numMaxLevel':0,
              'numMaxLevelUnique':0,
              'numMaxLevelRare':0,
              'numRare':0,
              'uniquePets': []}
      pets = self.pets
      data['numTotal'] = len(pets)
      uniques = []
      
      #update petdata if needed
      from zope.component import getUtility
      from esoth.wow.interfaces import IPetUtility
      petu = getUtility(IPetUtility)
      pkeys = petu.getPets().keys()
      newpids = [p['speciesId'] for p in pets if p['speciesId'] not in pkeys and p['speciesId'] != '0']
      if newpids:
        petu.addPetsById(newpids)
      petdata = petu.getPets()
      if not petdata:
        petu.populate()
        petdata = petu.getPets()
      
      updates = []
      for p in pets:
        self.predictPet(petdata,p)
        if p['level'] == '25':
          pbase = petdata[ p['speciesId'] ]
          if p['maxH'] != int(p['health']) or p['maxP'] != int(p['power']) or p['maxS'] != int(p['speed']):
            #updates.append(p)
            p['maxH'] = p['health']
            p['maxP'] = p['power']
            p['maxS'] = p['speed']
        if p['creatureName'] not in [u['creatureName'] for u in uniques]:
          uniques.append( p )
        elif int(p['qualityId']) > int([u['qualityId'] for u in uniques if u['creatureName'] == p['creatureName']][0]):
          uniques = [u for u in uniques if u['name'] != p['name']]
          uniques.append( p )
      #if updates:
      #  petu.updateBaseStats(updates)
      uniques.sort(lambda x,y: cmp(int(x['level']),int(y['level'])))
      data['numUnique'] = len(uniques)

      data['numMaxLevel'] = len( [p for p in pets if p['level'] == '25'] )
      data['numUniqueMaxLevel'] = len( [p for p in uniques if p['level'] == '25'] )
      data['numMaxLevelRare'] = len( [p for p in pets if p['level'] == '25' and p['qualityId'] == '3'] )
      data['numUniqueMaxLevelRare'] = len( [p for p in uniques if p['level'] == '25' and p['qualityId'] == '3'] )
      data['numUniqueRare'] = len( [p for p in uniques if p['qualityId'] == '3'] )
      data['numRare'] = len( [p for p in pets if p['qualityId'] == '3'] )

      data['uniquePets'] = uniques

      return data

    security.declarePublic('autoUpdateData')
    def autoUpdateData(self):
      from datetime import datetime
      now = datetime.now()
      if not self.lastupdated or now >= self.lastupdated+timedelta(days=1):
        self.updateData()
    
    def displaylastupdated(self):
      return self.lastupdated and self.lastupdated.strftime('%b %d, %Y %I:%M %p') or ''
    
class EditForm(dexterity.EditForm):
    grok.context(IGearPath)
    fields = field.Fields(IGearPath)
    fields['pets'].widgetFactory = DataGridFieldFactory