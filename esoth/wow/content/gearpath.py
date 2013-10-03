from datetime import datetime, timedelta
import json
from urllib import urlopen
from five import grok
import logging
from plone.dexterity.content import Item
from plone.directives import dexterity
from plone.namedfile.file import NamedImage as NamedImageFile
from zope.component import getUtility
from zope.interface import implements, Interface

from esoth.wow import _
from esoth.wow.content.config import cm_mounts, int_specs, spi_specs, str_specs, agi_specs, tank_specs, healer_specs, dps_specs, weapon_map, breedmap, armorMap
from esoth.wow.interfaces import IGearPath, IPetUtility, IMountUtility, servers

logger = logging.getLogger('esoth.wow')

class GearPath(Item):
    """ """
    implements(IGearPath)
    
    def gearMap(self):
      if not self.spec:
        return {}
      boss,slot,gear = self.getGear()
      _map = {}

      worn_slots = ['Weapon','Off Hand','Head','Neck','Shoulders','Back','Chest','Wrists','Hands','Waist','Legs','Feet','Ring1','Ring2','Trinket1','Trinket2']
      for k in worn_slots:
        item_type = k.replace('1','').replace('2','')
        count = len(slot.get(item_type,[]))
        itms = []
        for v in slot.get(item_type,[]):
          itm = {'name':v,
                 'ilvl':v.split('(')[-1].replace(')',''),
                 'icon':gear[v]['icon'],
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
      boss,slot,gear = self.getGear()
      heroicIlvls = set([535,541,566,572])
      normalIlvls = set([522,528,553,559])
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
      return [{'name':'Immerseus','tier':'tier15'},
              {'name':'The Fallen Protectors','tier':'tier15'},
              {'name':'Norushen','tier':'tier15'},
              {'name':'Sha of Pride','tier':'tier15'},
              {'name':'Galakras','tier':'tier15'},
              {'name':'Iron Juggernaut','tier':'tier15'},
              {'name':'Kor\'kron Dark Shaman','tier':'tier15'},
              {'name':'General Nazgrim','tier':'tier15'},
              {'name':'Malkorok','tier':'tier15'},
              {'name':'Spoils of Pandaria','tier':'tier15'},
              {'name':'Thok the Bloodthirsty','tier':'tier15'},
              {'name':'Siegecrafter Blackfuse','tier':'tier15'},
              {'name':'Paragons of the Klaaxi','tier':'tier15'},
              {'name':'Garrosh Hellscream','tier':'tier15'},
              {'name':'Ordos','tier':'tier15'},
              {'name':'Jin\'rokh','tier':'tier14'},
              {'name':'Horridon','tier':'tier14'},
              {'name':'Zandalari Council','tier':'tier14'},
              {'name':'Tortos','tier':'tier14'},
              {'name':'Megaera','tier':'tier14'},
              {'name':'Ji-Kun','tier':'tier14'},
              {'name':'Durumu','tier':'tier14'},
              {'name':'Primordius','tier':'tier14'},
              {'name':'Dark Animus','tier':'tier14'},
              {'name':'Iron Qon','tier':'tier14'},
              {'name':'Twin Consorts','tier':'tier14'},
              {'name':'Lei Shen','tier':'tier14'},
              {'name':'Ra-den','tier':'tier14'},
              {'name':'Shared - Throne of Thunder','tier':'tier14'},
              {'name':'Legendary','tier':'nontier'},
              {'name':'Leatherworking','tier':'nontier'},
              {'name':'Tailoring','tier':'nontier'},
              {'name':'Blacksmithing','tier':'nontier'}]
       
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
      
      if 'Ironforge' in [r['name'] for r in data['reputation']]:
        self.faction = 'Alliance'
      else:
        self.faction = 'Horde'
      
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
                 'Throne of Thunder',
                 'Siege of Orgrimmar']
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
      
      #
      _mounts = []
      for mount in data['mounts']['collected']:
        _mounts.append({'name':mount['name'],
                        'creatureId':mount['creatureId'],
                        'spellId':mount['spellId'],
                        'itemId':mount['itemId'],
                        'icon':mount['icon'],
                        'isCollected': True,
                        'isGround':mount['isGround'],
                        'isFlying':mount['isFlying'],
                        'isAquatic':mount['isAquatic'],
                        'isJumping':mount['isJumping']})
      self.mountDetails = _mounts

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
        p['maxH'] = int( round( 25 * (float(base['health']) + breedmap[p['breedId']]['health']) * rarity * 5 + 100 ))
        p['maxS'] = int( round( 25 * (float(base['speed']) + breedmap[p['breedId']]['speed']) * rarity ))
        p['maxP'] = int( round( 25 * (float(base['power']) + breedmap[p['breedId']]['power']) * rarity ))
  
    def applyClasses(self, m, default_faction, klass, cm_flag):
      klass = []
      faction = default_faction == 'Alliance' and 'A' or 'H'
      obtainable = 'Y'
      if m['restriction'] and m['restriction'] != klass:
        klass.append('restriction'); klass.append('restrictionHidden')
      klass.append(m.get('isCollected') and 'obtainedMount' or 'unobtainedMount')
      klass.append(m.get('faction',faction).lower() == 'a' and 'allianceMount' or m['faction'] == 'H' and 'hordeMount' or 'bothMount')
      if m.get('obtainable',obtainable).lower() == 'n' and not m['isCollected']: # no longer obtainable, but we have it
        klass.append('unobtainableMount'); klass.append('unobtainableMountHidden')
      elif cm_flag:
        klass.append('unobtainableMount'); klass.append('unobtainableMountHidden')
      else:
        klass.append('obtainableMount')
      klass.append(' '.join([m.get(k) and k or 'not'+k for k in ('isJumping','isGround','isFlying','isAquatic',)]))
      m = m.copy()
      m['classes'] = ' '.join(klass)
      return m
    
    def mountData(self):
      """ Combine json info on all mounts with collected mount info
      """
      resourceMounts = self.resources().mounts
      data = {}
      for rm in resourceMounts:
        data[ str(rm['spellId']) ] = rm
      
      mymounts = {}
      for m in self.mountDetails:
        mymounts[str(m['spellId'])] = m
      _mounts = []
      
      _cm_flag = False
      obt_cm_mounts = [m for m in mymounts.keys() if m in cm_mounts]
      for id,info in data.items():
        _mount = {'icon':info.get('icon'),
                  'isCollected':info.get('isCollected'),
                  'isGround':info.get('isGround'),
                  'isFlying':info.get('isFlying'),
                  'isAquatic':info.get('isAquatic'),
                  'isJumping':info.get('isJumping'),
                  'restriction':info.get('restriction'),
                  'spellId':id,
                  'name':info['name'],
                  'location':info['location'],
                  'obtainable':info['obtainable'],
                  'faction':info['faction']}
        mkeys = mymounts.keys()
        mkeys.sort()
          
        if id in mymounts:
          if mymounts[id]['name'] != info['name']:
            logger.warn('%s (import) vs %s (blizz)' % (info['name'],mymounts[id]['name']))
          if info['location'] == 'unknown':
            logger.warn('unknown location - %s' % info['name'])
          if info['faction'] == 'U':
            logger.warn('unknown faction - %s' % info['name'])
          if info['obtainable'] == 'U':
            logger.warn('unknown if obtainable - %s' % info['obtainable'])
          _mount.update({'isCollected':True,
                         'icon':mymounts[id]['icon'],
                         'name':mymounts[id]['name'],
                         'itemId':mymounts[id]['itemId'],
                         'isGround':mymounts[id]['isGround'],
                         'isFlying':mymounts[id]['isFlying'],
                         'isAquatic':mymounts[id]['isAquatic'],
                         'isJumping':mymounts[id]['isJumping']})
          if not data[id].get('icon'):
            data[id]['icon'] = mymounts[id]['icon']
            data[id]['isGround'] = mymounts[id]['isGround']
            data[id]['isFlying'] = mymounts[id]['isFlying']
            data[id]['isAquatic'] = mymounts[id]['isAquatic']
            data[id]['isJumping'] = mymounts[id]['isJumping']
        
        _cm_flag = id in cm_mounts and id not in obt_cm_mounts
        _mounts.append(self.applyClasses(_mount,self.faction,self.klass,_cm_flag))
      for id in mymounts.keys():
        # we don't have any data on this one
        if id not in data:
          logger.warn('added - %s' % id)
          data[id] = {'name':mymounts[id]['name'],'faction':'U','obtainable':'U','location':'unknown'}
          _mounts.append(self.applyClasses({'isCollected':True,
                          'icon':mymounts[id]['icon'],
                          'location':'unknown',
                          'faction':'U',
                          'obtainable':'U',
                          'spellId':id,
                          'restriction':'',
                          'itemId':mymounts[id]['itemId'],
                          'name':mymounts[id]['name'],
                          'isGround':mymounts[id]['isGround'],
                          'isFlying':mymounts[id]['isFlying'],
                          'isAquatic':mymounts[id]['isAquatic'],
                          'isJumping':mymounts[id]['isJumping']},self.faction,self.klass,_cm_flag))
            
      return _mounts
      
    def addPetsById(self, pids):
      pets = self.resources().pets
      base_url = 'http://us.battle.net/api/wow/battlePet/stats/%s?qualityId=0'
      for pid in pids:
        url = base_url % pid
        try:
          pdata = json.load(urlopen(url))
        except ValueError:
          pdata = json.load(urlopen('http://www.esoth.com/proxyw?u='+url))
        pets.append({'health': ( pdata['health'] - 100 ) / 5 - breedmap[ str(pdata['breedId']) ]['health'],
                     'speed' : pdata['speed'] - breedmap[ str(pdata['breedId']) ]['speed'],
                     'power' : pdata['power'] - breedmap[ str(pdata['breedId']) ]['power'],
                     'speciesId': pdata['speciesId'] })
      self.resources().pets = pets                   

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
      _resource = self.resources().pets
      petdata = {}
      pkeys = [p['speciesId'] for p in _resource]
      for p in _resource:
        petdata[ p['speciesId'] ] = p
      newpids = [p['speciesId'] for p in pets if p['speciesId'] not in pkeys and p['speciesId'] != '0']
      if newpids:
        self.addPetsById(newpids)
      
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
      
    def matchSpec(self,spec,g):
      if g['agility'] and spec not in agi_specs:
        return False
      if g['strength'] and spec not in str_specs:
        return False
      if g['intellect'] and spec not in int_specs:
        return False
      if g['spirit'] and spec not in spi_specs:
        return False
      if (g['dodge'] or g['parry']) and spec not in tank_specs:
        return False
      if g.get('dps_flag') and spec not in dps_specs:
        return False
      if g.get('healer_flag') and spec not in healer_specs:
        return False
      if g['klass'] and self.klass.lower() != g['klass'].lower():
        return False
      if g['armorClass'] and g['armorClass'] in armorMap and self.klass.lower() not in armorMap[ g['armorClass'] ]:
        if g['slot'] != 'Back': # Blizzard counts all backs as cloth
          return False
      if g['slot'] == 'Weapon':
        return spec in weapon_map[ g['weaponType'] ]
      return True
      
    def getGear(self):
      _gear = self.resources().gear
      boss = {} # boss[bossname][slot]=itemname
      slot = {}
      gear = {}
    
      for g in _gear:
       if self.spec:
        for spec in self.spec:
          if self.matchSpec(spec,g):
            for i,_id in zip(g['ilvls'],g['itemIds']):
              name = '%s (%s)' % (g['name'],i)
              if boss.has_key(g['source']):
                if boss[ g['source'] ].has_key(g['slot']):
                  boss[ g['source'] ][ g['slot'] ].append(name)
                else:
                  boss[ g['source'] ][ g['slot'] ] = [name]
              else:
                boss[ g['source'] ] = {g['slot']:[name]}
              
              if slot.has_key(g['slot']):
                slot[ g['slot'] ].append(name)
              else:
                slot[ g['slot'] ]=[name]
          
              item = {'boss':g['source'],'slot':g['slot'],'id':_id,'icon':g['icon']}
              gear[name] = item
      
      _sorter = lambda x,y: cmp(int(x.split('(')[-1].replace(')','')), int(x.split('(')[-1].replace(')','')))
      for k,v in slot.items():
        v.sort(_sorter)
        v.reverse()
        slot[k]=v
    
      return (boss,slot,gear)
    
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