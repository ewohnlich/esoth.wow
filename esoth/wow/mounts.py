from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from persistent.mapping import PersistentMapping
from interfaces import IPetUtility
import json, os

class MountUtility():
  implements(IMountUtility)
  
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
    for pid in pids:
      url = base_url % pid
      try:
        pdata = json.load(urllib2.urlopen(url))
      except ValueError:
        pdata = json.load(urllib2.urlopen('http://www.esoth.com/proxyw?u='+url))
      petdata[ str(pdata['speciesId']) ] = {'health': ( pdata['health'] - 100 ) / 5 - breedmap[ str(pdata['breedId']) ]['health'],
                                            'speed' : pdata['speed'] - breedmap[ str(pdata['breedId']) ]['speed'],
                                            'power' : pdata['power'] - breedmap[ str(pdata['breedId']) ]['power'], }
    json.dump(petdata,open(os.path.join(os.path.dirname(__file__),'pets.json'),'wb'))
    
  def updateBaseStats(self, updates):
    """ Update our base stat based on real level 25 pets that conflict with it """
    petdata = self.getPets()
    for upd in updates:
      rarity = int(upd['qualityId'])*.1+1
      health = ( float(upd['health']) - 100 ) / 25 / rarity / 5 - breedmap[ upd['breedId'] ]['health']
      speed = float(upd['speed']) / 25 / rarity - breedmap[ upd['breedId'] ]['speed']
      power = float(upd['power']) / 25 / rarity - breedmap[ upd['breedId'] ]['power']
      
      petdata[ upd['speciesId'] ] = {'health': health,
                                     'speed' : speed,
                                     'power' : power, }
    json.dump(petdata,open(os.path.join(os.path.dirname(__file__),'pets.json'),'wb'))
  
  def getPets(self):
    petdata = json.load(open(os.path.join(os.path.dirname(__file__),'pets.json')))
    return petdata