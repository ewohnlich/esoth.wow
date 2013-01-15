from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from persistent.mapping import PersistentMapping
from interfaces import IPetUtility
import json, os, urllib2

class PetUtility():
  implements(IPetUtility)
  
  def __init__(self):
    self.petdata = PersistentMapping()
  
  def populate(self):
    # populates from current pets in portal
    
    petids = []
    portal = getUtility(ISiteRoot)
    for b in getToolByName(portal,'portal_catalog')(portal_type='WoWChar'):
      pets = [p['speciesId'] for p in b.pets if p.get('speciesId') and p['speciesId'] not in petids and p['speciesId'] != '0']
      petids.extend(pets)
    
    self.addPetsById(petids)
        
  def addPetsById(self, pids):
    petdata = self.getPets()
    base_url = 'http://us.battle.net/api/wow/battlePet/stats/%s?qualityId=0'
    breedmap = {'3' : {'health':0.5,'power':0.5,'speed':0.5},
                '13': {'health':0.5,'power':0.5,'speed':0.5},
                '4' : {'health':0,  'power':2,  'speed':0},
                '14': {'health':0,  'power':2,  'speed':0},
                '5' : {'health':0,  'power':0,  'speed':2},
                '15': {'health':0,  'power':0,  'speed':2},
                '6' : {'health':2,  'power':0,  'speed':0},
                '16': {'health':2,  'power':0,  'speed':0},
                '7' : {'health':0.9,'power':0.9,'speed':0},
                '17': {'health':0.9,'power':0.9,'speed':0},
                '8' : {'health':0,  'power':0.9,'speed':0.9},
                '18': {'health':0,  'power':0.9,'speed':0.9},
                '9' : {'health':0.9,'power':0,  'speed':0.9},
                '19': {'health':0.9,'power':0,  'speed':0.9},
                '10': {'health':0.4,'power':0.9,'speed':0.4},
                '20': {'health':0.4,'power':0.9,'speed':0.4},
                '11': {'health':0.4,'power':0.4,'speed':0.9},
                '21': {'health':0.4,'power':0.4,'speed':0.9},
                '12': {'health':0.9,'power':0.4,'speed':0.4},
                '22': {'health':0.9,'power':0.4,'speed':0.4}, }
    for pid in pids:
      url = base_url % pid
      pdata = json.load(urllib2.urlopen(url))
      petdata[ str(pdata['speciesId']) ] = {'health': ( pdata['health'] - 100 ) / 5 - breedmap[ str(pdata['breedId']) ]['health'],
                                            'speed' : pdata['speed'] - breedmap[ str(pdata['breedId']) ]['speed'],
                                            'power' : pdata['power'] - breedmap[ str(pdata['breedId']) ]['power'], }
    json.dump(petdata,open(os.path.join('var','pets.json'),'wb'))
  
  def getPets(self):
    petdata = json.load(open(os.path.join('var','pets.json')))
    return petdata