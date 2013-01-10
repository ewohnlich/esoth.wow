# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes import ATCTMessageFactory as _
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import RFC822Marshaller
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent, registerATCT
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.Archetypes.atapi import AnnotationStorage
from Products.CMFCore.permissions import View
from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.Column import Column
from esoth.wow.config import PROJECTNAME
from esoth.wow.interfaces import IWoWChar
from zope.interface import implements

WoWCharSchema = ATContentTypeSchema.copy() + Schema((
    StringField('server',
        required = True,
        widget = StringWidget(
            label= u'Server'),
    ),
    LinesField('groups',
        widget=LinesWidget(label='Groups',)
        ),
    BooleanField('alt',
        widget=BooleanWidget(label='Alt?',)
        ),
    StringField('race',
        required = False,
        vocabulary='raceSelection',
        widget = SelectionWidget(visible={'edit':'hidden'}),
    ),
    StringField('gender',
        required = False,
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('level',
        required = False,
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('class',
        required = False,
        vocabulary='classSelection',
        widget = SelectionWidget(visible={'edit':'hidden'}),
    ),
    StringField('titles',
        required = False,
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    DataGridField('pets',
        widget = DataGridWidget(label = 'Pets',
                     columns = {
                    'name' :       Column(_(u"Tier")),
                    'creatureName':Column(_(u"Creature Name")),
                    'spellId' :    Column(_(u"Column")),
                    'creatureId' : Column(_(u"ID")),
                    'qualityId' :  Column(_(u"Name")),
                    'icon' :       Column(_(u"Icon")),
                    'breedId' :    Column(_(u"Can Battle")),#stats
                    'level' :      Column(_(u"Can Battle")),
                    'health' :     Column(_(u"Can Battle")),
                    'power' :      Column(_(u"Can Battle")),
                    'speed' :      Column(_(u"Can Battle")),
                    'canBattle' :  Column(_(u"Can Battle")),
                      }),
        columns = ('name','creatureName','spellId','creatureId','qualityId','icon','breedId','level','health','power','speed','canBattle',),
    ),
    StringField('mounts',
        required = False,
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('guild',
        required = False,
        widget = StringWidget(
            label= u'Guild'),
    ),
    DataGridField('specs',
                searchable=True, # One unit tests checks whether text search works
                widget = DataGridWidget(label = 'Main Spec',visible={'edit':'hidden'},
                     columns={
                        'name' : Column(_(u"Name")),
                        'icon': Column(_(u"Icon")),}),
                columns=('name','icon'),
            ),
    DataGridField('mainTalents',
        widget = DataGridWidget(label = 'Main Talents',
                     columns = {
                    'tier' : Column(_(u"Tier")),
                    'column' : Column(_(u"Column")),
                    'id' : Column(_(u"ID")),
                    'name' : Column(_(u"Name")),
                    'icon' : Column(_(u"Icon")),}),
        columns = ('tier','column','id','name','icon'),
    ),
    DataGridField('secondTalents',
        widget = DataGridWidget(label = 'Second Talents',
                     columns = {
                    'tier' : Column(_(u"Tier")),
                    'column' : Column(_(u"Column")),
                    'id' : Column(_(u"ID")),
                    'name' : Column(_(u"Name")),
                    'icon' : Column(_(u"Icon")),}),
        columns = ('tier','column','id','name','icon'),
    ),
    ImageField('avatar',
        required = False,
        storage = AnnotationStorage(migrate=True),
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (170, 170),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
               },
        widget = ImageWidget(
            label= u'Avatar (upload)'),

    ),
    IntegerField('points',
        widget = IntegerWidget(visible={'edit':'hidden'}),
    ),
    DataGridField('progression',
        widget = DataGridWidget(label = 'Progression',
                     columns = {
                    'tier' : Column(_(u"Tier")),
                    'raid' : Column(_(u"Raid")),
                    'boss' : Column(_(u"Boss")),
                    'nkills':Column(_(u"Normal Kills")),
                    'hkills':Column(_(u"Heroic Kills"))}),
        columns = ('tier','raid','boss','nkills','hkills'),
    ),
    DateTimeField('cacheDate',
        widget = CalendarWidget(visible={'edit':'hidden'}),
    ),
    StringField('agility',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('strength',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('intellect',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('spirit',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('stamina',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('crit',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('haste',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('mastery',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('hit',
        widget = StringWidget(visible={'edit':'hidden'}),
    ),

  ),
  marshall=RFC822Marshaller()
  )

WoWCharSchema.changeSchemataForField('agility','stats')
WoWCharSchema.changeSchemataForField('strength','stats')
WoWCharSchema.changeSchemataForField('intellect','stats')
WoWCharSchema.changeSchemataForField('spirit','stats')
WoWCharSchema.changeSchemataForField('stamina','stats')
WoWCharSchema.changeSchemataForField('crit','stats')
WoWCharSchema.changeSchemataForField('haste','stats')
WoWCharSchema.changeSchemataForField('mastery','stats')
WoWCharSchema.changeSchemataForField('hit','stats')

class WoWChar(ATCTContent):
    schema = WoWCharSchema
    implements(IWoWChar)

    security = ClassSecurityInfo()

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = 'Album art'
        return self.getField('avatar').tag(self, **kwargs)

    security.declareProtected(View, 'raceSelection')
    def raceSelection(self):
      return ('Draenei','Dwarf','Gnome','Human','Night Elf','Worgen','Pandaren',
              'Blood Elf','Goblin','Orc','Tauren','Troll','Undead')

    security.declareProtected(View, 'classSelection')
    def classSelection(self):
      return ('Death Knight','Druid','Hunter','Mage','Monk','Paladin','Priest','Rogue','Shaman','Warlock','Warrior')

    security.declareProtected(View, 'hasAvatar')
    def hasAvatar(self):
      """ check this before making an image tag """
      return self.getAvatar() and True or False

    def progressionDisplay(self):
      prog = self.getProgression()

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

    security.declarePublic('updateData')
    def updateData(self):
      import json
      from urllib2 import urlopen
      from DateTime import DateTime
      base_url = 'http://us.battle.net/api/wow/character/%s/%s?fields=guild,talents,stats,items,reputation,professions,appearance,companions,mounts,pets,achievements,progression,titles'
      base_image_url = 'http://us.battle.net/static-render/us/'

      server = self.getServer().lower().replace("'","").replace(' ','%20')
      charname = self.Title().lower()

      url = base_url % (server,charname)
      _json = json.load(urlopen(url))

      # general
      self.setCacheDate(DateTime())
      try:
        self.setLevel(_json['level'])
      except:
        return
      racemap = {'1':'Human','5':'Undead','11':'Draenei','7':'Gnome','8':'Troll','4':'Night Elf','2':'Orc','3':'Dwarf','10':'Blood Elf','22':'Worgen','6':'Tauren','9':'Goblin','25':'Pandaren','26':'Pandaren'}
      self.setRace(racemap[str(_json['race'])])
      self.setClass(['none','Warrior','Paladin','Hunter','Rogue','Priest','Death Knight','Shaman','Mage','Warlock','Monk','Druid'][_json['class']])
      self.setGender(_json['gender'] and 'Female' or 'Male')
      img = urlopen(base_image_url+_json['thumbnail']).read()
      self.setAvatar(img)
      self.setPoints(_json['achievementPoints'])

      # talents
      talents = _json['talents']
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
          self.setMainTalents(_talents)
          specs.insert(0,_spec)
        else:
          self.setSecondTalents(_talents)
          specs.append(_spec)
      self.setSpecs(specs)

      if _json.get('guild'):
        self.setGuild(_json['guild']['name'])

      # stats
      self.setAgility(_json['stats']['agi'])
      self.setStrength(_json['stats']['str'])
      self.setIntellect(_json['stats']['int'])
      self.setSpirit(_json['stats']['spr'])
      self.setStamina(_json['stats']['sta'])
      self.setCrit(_json['stats']['critRating'])
      self.setHaste(_json['stats']['hasteRating'])
      self.setMastery(_json['stats']['masteryRating'])
      self.setHit(_json['stats']['hitRating'])

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
      raids = _json['progression']['raids']
      progression = []
      for raid in raids:
        for boss in raid['bosses']:
          if raid['name'] in tiermap:
            if boss['name'] not in [b['boss'] for b in progression] or boss['name'] == 'Ragnaros':
              # Ragnaros is broken and lists heroic kills independently
              progression.append({'tier':str(tiermap.index(raid['name'])),
                                  'raid':raid['name'],
                                  'boss':boss['name'],
                                  'nkills':str(boss['normalKills']),
                                  'hkills':str(boss['heroicKills'])})
      progression.sort(lambda x,y: cmp(x['tier'],y['tier']))
      self.setProgression(progression)

      # companions
      pets = _json['pets']
      total = pets['numCollected']
      _pets = []
      for pet in pets['collected']:
        _pets.append({'name':pet['name'],
                      'creatureName':pet['creatureName'],
                      'spellId':str(pet['spellId']),
                      'creatureId':str(pet['creatureId']),
                      'qualityId':str(pet['stats']['petQualityId']),
                      'icon':pet['icon'],
                      'breedId':str(pet['stats']['breedId']),
                      'level':str(pet['stats']['level']),
                      'health':str(pet['stats']['health']),
                      'power':str(pet['stats']['power']),
                      'speed':str(pet['stats']['speed']),
                      'canBattle':pet['canBattle'] and 'True' or 'False'} )
      self.setPets(_pets)

      # mounts
      self.setMounts(_json['mounts']['numCollected'])

      # titles
      self.setTitles(len(_json['titles']))

      self.reindexObject()

    security.declarePublic('numcompanions')
    def numcompanions(self):
      names = [p.get('creatureName') for p in self.getPets()]
      uniques = {}.fromkeys(names).keys()
      return len( uniques )

    security.declarePublic('petData')
    def petData(self):
      data = {'numUnique':0,
              'numTotal':0,
              'numMaxLevel':0,
              'numMaxLevelUnique':0,
              'numMaxLevelRare':0,
              'numRare':0,
              'uniquePets': []}
      pets = self.getPets()
      data['numTotal'] = len(pets)

      breedmap = {'3' : = {'health':0.5,'power':0.5,'speed':0.5},
                  '13': = {'health':0.5,'power':0.5,'speed':0.5},
                  '4' : = {'health':0,  'power':2,  'speed':0},
                  '14': = {'health':0,  'power':2,  'speed':0},
                  '5' : = {'health':0,  'power':0,  'speed':2},
                  '15': = {'health':0,  'power':0,  'speed':2},
                  '6' : = {'health':2,  'power':0,  'speed':0},
                  '16': = {'health':2,  'power':0,  'speed':0},
                  '7' : = {'health':0.9,'power':0.9,'speed':0},
                  '17': = {'health':0.9,'power':0.9,'speed':0},
                  '8' : = {'health':0,  'power':0.9,'speed':0.9},
                  '18': = {'health':0,  'power':0.9,'speed':0.9},
                  '9' : = {'health':0.9,'power':0,  'speed':0.9},
                  '19': = {'health':0.9,'power':0,  'speed':0.9},
                  '10': = {'health':0.4,'power':0.9,'speed':0.4},
                  '20': = {'health':0.4,'power':0.9,'speed':0.4},
                  '11': = {'health':0.4,'power':0.4,'speed':0.9},
                  '21': = {'health':0.4,'power':0.4,'speed':0.9},
                  '12': = {'health':0.9,'power':0.4,'speed':0.4},
                  '22': = {'health':0.9,'power':0.4,'speed':0.4}, }
      uniques = []
      for p in pets:
        if p['creatureName'] not in [u['creatureName'] for u in uniques]:
          uniques.append( p )
        elif int(p['qualityId']) > int([u['qualityId'] for u in uniques if u['creatureName'] == p['creatureName']][0]):
          uniques = [u for u in uniques if u['name'] != p['name']]
          #leveldiff = 25-int(p['level'])
          #rarity = int(p['petQualityId'])*.1+1
          # hmm, will need to get base pet numbers and store them somewhere for this. Blech
          #p['maxH'] = leveldiff * (basep + breedmap[p['breedId']]['health'])
          #p['maxS'] = leveldiff * (basep + breedmap[p['breedId']]['speed'])
          #p['maxP'] = leveldiff * (basep + breedmap[p['breedId']]['power'])
          uniques.append( p )
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
      from DateTime import DateTime
      now = DateTime()
      if not self.getCacheDate() or now >= self.getCacheDate()+1:
        self.updateData()

registerATCT(WoWChar, PROJECTNAME)