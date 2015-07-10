from urllib2 import urlopen, URLError
import json
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from esoth.wow import _
from esoth.wow.config import API_KEY

weaponSubClass = {'0':'One-Hand Axe',
                  '1':'Two-Hand Axe',
                  '2':'Bow',
                  '3':'Gun',
                  '4':'One-Hand Mace',
                  '5':'Two-Hand Mace',
                  '6':'Polearm',
                  '7':'One-Hand Sword',
                  '8':'Two-Hand Sword',
                  '9':'Obsolete',
                  '10':'Staff',
                  '11':'Exotic',
                  '12':'Exotic',
                  '13':'Fist Weapon',
                  '14':'Miscellaneous',
                  '15':'Dagger',
                  '16':'Thrown',
                  '17':'Spear',
                  '18':'Crossbow',
                  '19':'Wand',
                  '20':'Fishing Pole'}

armorSubClass = ['Miscellaneous','Cloth','Leather','Mail','Plate','Cosmetic','Shield']

statmap = {'3':'agility',
           '36':'haste',
           '31':'hit',
           '7':'stamina',
           '49':'mastery',
           '59':'multistrike',
           '40':'versatility',
           '5':'intellect',
           '6':'spirit',
           '32':'crit',
           '4':'strength',
           '13':'dodge',
           '14':'parry',
           '73':'agility-intellect'}

inventoryType = {'1':'Head',
                 '2':'Neck',
                 '3':'Shoulders',
                 '4':'Shirt',
                 '5':'Chest',
                 '6':'Waist',
                 '7':'Legs',
                 '8':'Feet',
                 '9':'Wrists',
                 '10':'Hands',
                 '11':'Ring',
                 '12':'Trinket',
                 '13':'Weapon',
                 '14':'Off-Hand',
                 '15':'Weapon',
                 '16':'Back',
                 '17':'Weapon',
                 '18':'Bag',
                 '19':'Tabard',
                 '20':'Chest',
                 '21':'Weapon',
                 '22':'Off-Hand',
                 '23':'Off-Hand',
                 '24':'Ammo',
                 '25':'Thrown',
                 '26':'Weapon',
                 '27':'Relic'}

allowableClasses = ['None','Warrior','Paladin','Hunter','Rogue','Priest','Death Knight','Shaman','Mage','Warlock','Monk','Druid']

character_url = 'https://%(region)s.api.battle.net/wow/character/%(realm)s/%(character)s?apikey=%(api_key)s&fields=items,progression'
item_url = 'https://us.api.battle.net/wow/item/%(item)s?apikey=%(api_key)s'

def process_context(blizz): # accepts blizzard json data
  data = {'weapon_type':'','klass':''}
  data['name'] = blizz['name']
  if blizz.get('weaponInfo'):
    data['weapon_type'] = weaponSubClass[ str(blizz['itemSubClass']) ]
  data['armor_class'] = blizz['itemSubClass'] < len(armorSubClass) and armorSubClass[ blizz['itemSubClass'] ] or ''
  data['icon'] = blizz['icon']
  for s in blizz['bonusStats']:
    if statmap.get( str(s['stat']) ):
      for substat in statmap.get( str(s['stat']) ).split('-'): # i.e. agility-intellect
        data[substat] = s['amount']
  data['slot'] = inventoryType.get( str(blizz['inventoryType']) )
  data['ilvl'] = blizz['itemLevel']
  if blizz.get('allowableClasses'):
    data['klass'] = allowableClasses[ blizz['allowableClasses'][0] ]
  for stat in ['agility','strength','intellect','crit','haste','mastery','multistrike','versatility']:
    if not data.get(stat):
      data[stat] = 0
  return data

def get_item(id):
  url = item_url % {'item':id,'api_key':API_KEY}
  blizz = get_api(url)
  contexts = []
  if not [c for c in blizz['availableContexts'] if c]:
    data = {'gear_context':'vendor'} # legendary ring
    data.update(process_context(blizz))
    contexts.append(data)
  else:
    for context in blizz['availableContexts']:
      context_url = '/%s?'.join(url.split('?')) % context
      blizz = get_api(context_url)
      data = {'gear_context':context}
      data.update(process_context(blizz))
      contexts.append(data)

      # add warforged
      data = data.copy()
      data['gear_context'] = '%s (w)' % context
      for bonus in blizz['bonusSummary']['bonusChances']:
        if bonus['chanceType'] == 'UPGRADE':
          for stat in bonus['stats']:
            if stat['statId'] in statmap:
              for substat in statmap[stat['statId']].split('-'): # i.e. agility-intellect
                data[substat] += stat['delta']
      contexts.append(data)

  return contexts

def context_name(context):
  if not context:
    return ''
  context = context.replace('(w) (s)','(W+S)')
  context = context.replace('(w)','(W)')
  context = context.replace('(s)','(S)')
  context = context.replace('raid-normal','Normal')
  context = context.replace('raid-heroic','Heroic')
  context = context.replace('raid-mythic','Mythic')
  return context

def get_character(region,realm,character):
  url = character_url % {'region':region,'realm':realm,'character':character,'api_key':API_KEY}
  blizz = get_api(url)
  return blizz

def get_api(url):
  base_url = url
  try:
    blizz = json.load(urlopen(url))
  except (URLError, IOError):
    try:
      url = base_url.replace('https://us.api.battle.net/wow','https://warcrafttools.com/bnet/wow')
      blizz = json.load(urlopen(url))
    except:
      url = 'http://www.esoth.com/proxyw?u='+base_url
      blizz = json.load(urlopen(url))
  return blizz

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
  slugs = [r['slug'] for r in realms]
  for r in json.load(urlopen('http://eu.battle.net/api/wow/realm/status'))['realms']:
    if r['slug'] not in slugs:
      realms.append(r)
except:
  try:
    realms = json.load(urlopen('http://www.esoth.com/proxyw?u=http://us.battle.net/api/wow/realm/status'))['realms']
    slugs = [r['slug'] for r in realms]
    for r in json.load(urlopen('http://www.esoth.com/proxyw?u=http://eu.battle.net/api/wow/realm/status'))['realms']:
      if r['slug'] not in slugs:
        realms.append(r)
  except:
    pass
servers = SimpleVocabulary([SimpleTerm(value=r['slug'], title=_('%s' % r['name'])) for r in realms])

def get_icon(icon_tag,avatar=False):
  if avatar:
    #return 'http://us.battle.net/static-render/us/%s.jpg' % icon_tag
    return 'http://www.esoth.com/proxyi?u=http://us.battle.net/static-render/us/%s' % icon_tag
  else:
    #return 'http://us.media.blizzard.com'
    return 'http://www.esoth.com/proxyi?u=http://us.media.blizzard.com/wow/icons/18/%s.jpg' % icon_tag