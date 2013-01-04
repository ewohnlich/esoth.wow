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
    DataGridField('specs',
                searchable=True, # One unit tests checks whether text search works
                widget = DataGridWidget(label = 'Main Spec',
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
    LinesField('progression',
        widget = DataGridWidget(label = 'Progression',
                     columns = {
                    'tier' : Column(_(u"Tier")),
                    'raid' : Column(_(u"Raid")),
                    'boss' : Column(_(u"Boss")),
                    'nkills':Column(_(u"Normal Kills")),
                    'hkills':Column(_(u"Heroic Kills"))}),
        columns = ('tier','column','id','name','icon'),
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
WoWCharSchema.changeSchemataForField('tier14','progression')
WoWCharSchema.changeSchemataForField('tier15','progression')

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
              'Al\'Akir',,)
    
    security.declareProtected(View, 'tier12bosses')
    def tier12bosses(self):
      return ('Shannox',
              'Lord Rhyolith',
              'Alysrazor',
              'Beth\'tilac',
              'Baleroc',
              'Majordomo Staghelm',
              'Ragnaros',)
    
    security.declareProtected(View, 'tier13bosses')
    def tier13bosses(self):
      return ('Morchok',
              'Warlord Zon\'ozz',
              'Yor\'sahj the Unsleeping',
              'Hagara the Stormbinder',
              'Ultraxion',
              'Warmaster Blackhorn',
              'Spine of Deathwing',
              'Madness of Deathwing')

    security.declarePublic('updateData')
    def updateData(self):
      import json
      from urllib import urlopen
      from DateTime import DateTime
      base_url = 'http://www.esoth.com/proxyw?u=http://us.battle.net/api/wow/character/%s/%s?fields=talents,stats,items,reputation,titles,professions,appearance,companions,mounts,pets,achievements,progression,titles'
      base_image_url = 'http://www.esoth.com/proxyi?u=http://us.battle.net/static-render/us/'

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
          progression.append({'tier':tiermap.index(raid['name']),
                              'raid':raid['name'],
                              'boss':boss['name'],
                              'nkils':boss['normalKills'],
                              'hkills':boss['heroicKills']})
      progression.sort(lambda x,y: cmp(x['tier'],y['tier']))
      self.setProgression(progression)
      
      # companions
      pets = _json['pets']
      total = pets['numCollected']
      names = [p['name'] for p in pets['collected']]
      uniques = {}.fromkeys(names).keys()
      self.setCompanions('%d unique (%d total)' % (len(uniques),total)
      
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

registerATCT(WoWChar, PROJECTNAME)