from datetime import datetime, timedelta
import json
from urllib import urlopen
from five import grok
from plone.dexterity.content import Item
from plone.directives import dexterity
from plone.namedfile.file import NamedImage as NamedImageFile
from zope.component import getUtility
from zope.interface import implements, Interface

from esoth.wow import _
from esoth.wow.content.gear import getGear
from esoth.wow.interfaces import IGearPath, IPetUtility, servers
from esoth.wow.pets import breedmap

class GearPath(Item):
    """ """
    implements(IGearPath)
    meta_type = 'GearPath'
    
    def gearMap(self):
      if not self.spec:
        return {}
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
      return ['Jin\'rokh','Horridon','Zandalari Council','Tortos','Megaera','Ji-Kun','Durumu','Primordius','Dark Animus','Iron Qon','Twin Consorts','Lei Shen','Ra-den','Shared - Throne of Thunder','Legendary']

       
    def updateData(self):
      base_image_url = 'http://us.battle.net/static-render/us/'
      url = 'http://us.battle.net/api/wow/character/%s/%s?fields=guild,talents,stats,items,reputation,professions,appearance,companions,mounts,pets,achievements,progression,titles' % (self.server,self.title.lower())
      equipped = set([])
      try:
        data = json.load(urlopen(url))
      except:
        url = 'http://www.esoth.com/proxyw?u='+url
        data = json.load(urlopen(url))
      try:
        gear = data['items']
      except KeyError:
        return 'bad'
      
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
      if self.server: # won't exist yet on creation
        return servers.getTerm(self.server).title
      
    def hasAvatar(self):
      """ check this before making an image tag """
      return bool(self.avatar)

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

    def autoUpdateData(self):
      from datetime import datetime
      now = datetime.now()
      if not self.lastupdated or now >= self.lastupdated+timedelta(days=1):
        return self.updateData()
    
    def displaylastupdated(self):
      return self.lastupdated and self.lastupdated.strftime('%b %d, %Y %I:%M %p') or ''
    
class Edit(dexterity.EditForm):
    grok.context(IGearPath)
    
    def updateFields(self):
      super(Edit, self).updateFields()
      for f in ['pets','mountDetails','mainTalents','secondTalents','specs','progression','acquiredItems','bisItems','downgradeItems','lastupdated']:
        if f in self.fields.keys():
          del self.fields[f]

class Add(dexterity.AddForm):
    grok.context(IGearPath)
    grok.name('GearPath')
    
    def updateFields(self):
      super(Add, self).updateFields()
      for f in ['pets','mountDetails','mainTalents','secondTalents','specs','progression','acquiredItems','bisItems','downgradeItems','lastupdated']:
        if f in self.fields.keys():
          del self.fields[f]