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
from esoth.wow.config import PROJECTNAME
from esoth.wow.interfaces import IWoWChar
from zope.interface import implements

WoWCharSchema = ATContentTypeSchema.copy() + Schema((
    StringField('server',
        required = True,
        widget = StringWidget(
            label= u'Server'),
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
    StringField('companions',
        required = False,
        widget = StringWidget(visible={'edit':'hidden'}),
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
    StringField('mainspec',
        required = False,
        widget = StringWidget(visible={'edit':'hidden'}),
    ),
    StringField('secondspec',
        required = False,
        widget = StringWidget(visible={'edit':'hidden'}),
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
    LinesField('tier11',
        required = False,
        vocabulary='tier11bosses',
        widget = MultiSelectionWidget(visible={'edit':'hidden'}),
    ),
    LinesField('tier12',
        required = False,
        vocabulary='tier12bosses',
        widget = MultiSelectionWidget(visible={'edit':'hidden'}),
    ),
    LinesField('tier13',
        required = False,
        vocabulary='tier13bosses',
        widget = MultiSelectionWidget(visible={'edit':'hidden'}),
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
WoWCharSchema.changeSchemataForField('tier11','progression')
WoWCharSchema.changeSchemataForField('tier12','progression')
WoWCharSchema.changeSchemataForField('tier13','progression')

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
    
    security.declareProtected(View, 'tier11bosses')
    def tier11bosses(self):
      return ('Toxitron',
              'Magmaw',
              'Maloriak',
              'Atramedes',
              'Chimaeron',
              'Nefarian',
              'Halfus Wyrmbreaker',
              'Valiona',
              'Elementium Monstrosity',
              'Cho\'gall',
              'Conclave of Wind',
              'Al\'Akir',
              'Toxitron (Heroic)',
              'Magmaw (Heroic)',
              'Maloriak (Heroic)',
              'Atramedes (Heroic)',
              'Chimaeron (Heroic)',
              'Nefarian (Heroic)',
              'Halfus Wyrmbreaker (Heroic)',
              'Valiona (Heroic)',
              'Elementium Monstrosity (Heroic)',
              'Cho\'gall (Heroic)',
              'Sinestra (Heroic)',
              'Conclave of Wind (Heroic)',
              'Al\'Akir (Heroic)',)
    
    security.declareProtected(View, 'tier12bosses')
    def tier12bosses(self):
      return ('Shannox',
              'Lord Rhyolith',
              'Alysrazor',
              'Beth\'tilac',
              'Baleroc',
              'Majordomo Staghelm',
              'Ragnaros',
              'Shannox (Heroic)',
              'Lord Rhyolith (Heroic)',
              'Alysrazor (Heroic)',
              'Beth\'tilac (Heroic)',
              'Baleroc (Heroic)',
              'Majordomo Staghelm (Heroic)',
              'Ragnaros (Heroic)',)
    
    security.declareProtected(View, 'tier13bosses')
    def tier13bosses(self):
      return ('Morchok',
              'Warlord Zon\'ozz',
              'Yor\'sahj the Unsleeping',
              'Hagara the Stormbinder',
              'Ultraxion',
              'Warmaster Blackhorn',
              'Spine of Deathwing',
              'Madness of Deathwing',
              'Morchok (Heroic)',
              'Warlord Zon\'ozz (Heroic)',
              'Yor\'sahj the Unsleeping (Heroic)',
              'Hagara the Stormbinder (Heroic)',
              'Ultraxion (Heroic)',
              'Warmaster Blackhorn (Heroic)',
              'Spine of Deathwing (Heroic)',
              'Madness of Deathwing (Heroic)',)

    security.declarePublic('updateData')
    def updateData(self):
      import json
      from urllib import urlopen
      from DateTime import DateTime
      base_url = 'http://us.battle.net/api/wow/character/%s/%s?fields=talents,stats,items,reputation,titles,professions,appearance,companions,mounts,pets,achievements,progression,titles'
      base_image_url = 'http://us.battle.net/static-render/us/'

      server = self.getServer().lower().replace("'","")
      charname = self.Title().lower()
      
      _json = json.load(urlopen(base_url % (server,charname)))
      
      # general
      self.setCacheDate(DateTime())
      self.setLevel(_json['level'])
      racemap = {'1':'Human','5':'Undead','11':'Draenei','7':'Gnome','8':'Troll','4':'Night Elf','2':'Orc','3':'Dwarf','10':'Blood Elf','22':'Worgen','6':'Tauren','9':'Goblin'}
      self.setRace(racemap[str(_json['race'])])
      self.setClass(['none','Warrior','Paladin','Hunter','Rogue','Priest','Death Knight','Shaman','Mage','Warlock','Monk','Druid'][_json['class']])
      self.setGender(_json['gender'] and 'Female' or 'Male')
      img = urlopen(base_image_url+_json['thumbnail']).read()
      self.setAvatar(img)
      self.setPoints(_json['achievementPoints'])
      
      # talents
      mainspec = '/'.join([str(t['total']) for t in _json['talents'][0]['trees']])
      self.setMainspec(mainspec)
      if len(_json['talents'])>1:
        secondspec = '/'.join([str(t['total']) for t in _json['talents'][1]['trees']])
        self.setSecondspec(secondspec)
        
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
      raids = _json['progression']['raids']
      tier13 = []
      tier12 = []
      tier11 = []
      for raid in raids:
        if raid['name']=='Dragon Soul':
          tier13.append(raid.copy())
        elif raid['name']=='Firelands':
          tier12.append(raid.copy())
        elif raid['name']=='Throne of the Four Winds':
          tier11.append(raid.copy())
        elif raid['name']=='The Bastion of Twilight':
          tier11.append(raid.copy())
        elif raid['name']=='Blackwing Descent':
          tier11.append(raid.copy())
      self.updateProgression('tier13',tier13)
      self.updateProgression('tier12',tier12)
      self.updateProgression('tier11',tier11)
      
      # companions
      self.setCompanions(len(_json['companions']))
      
      # mounts
      self.setMounts(len(_json['mounts']))
      
      # titles
      self.setTitles(len(_json['titles']))
      
      self.reindexObject()
      
    security.declarePublic('autoUpdateData')
    def autoUpdateData(self):
      from DateTime import DateTime
      now = DateTime()
      if not self.getCacheDate() or now >= self.getCacheDate()+1:
        self.updateData()
        
    security.declareProtected(View,'specTitle')
    def specTitle(self,specstring):
      specs = {'Death Knight':('Blood','Frost','Unholy'),
                'Druid':('Balance','Feral','Restoration'),
                'Hunter':('Beast Master','Marksmanship','Survival'),
                'Mage':('Arcane','Fire','Frost'),
                'Monk':('Brewmaster','Mistweaver','Windwalker'),
                'Paladin':('Holy','Protection','Retribution'),
                'Priest':('Discipline','Holy','Shadow'),
                'Rogue':('Assassination','Combat','Subtlety'),
                'Shaman':('Elemental','Enhancement','Restoration'),
                'Warlock':('Affliction','Demonology','Destruction'),
                'Warrior':('Arms','Fury','Protection')}
      trees = specstring.split('/')
      if int(trees[0])>int(trees[1]) and int(trees[0])>int(trees[2]):
        return specs[self.getClass()][0]
      elif int(trees[1])>int(trees[2]):
        return specs[self.getClass()][1]
      else:
        return specs[self.getClass()][2]
        
    security.declarePublic('updateProgression')
    def updateProgression(self,tier,raids):
      normalKills = []
      heroicKills = []
      for raid in raids:
        for boss in raid['bosses']:
          if boss['normalKills']>0:
            normalKills.append(boss['name'])
          if boss['heroicKills']>0:
            heroicKills.append(boss['name'])
      for hk in heroicKills:
        normalKills.append('%s (Heroic)' % hk)
      if tier == 'tier13':
        self.setTier13(normalKills)
      elif tier == 'tier12':
        self.setTier12(normalKills)
      elif tier == 'tier11':
        self.setTier11(normalKills)          

registerATCT(WoWChar, PROJECTNAME)