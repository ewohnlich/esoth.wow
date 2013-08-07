from five import grok
import json
import os
from plone.directives import form
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from urllib import urlopen
from z3c.form import button
from zope import schema

from esoth.wow import _
from esoth.wow.interfaces import IWoWResources, IGearSchema, IMountResourceSchema, IPetResourceSchema
from config import statmap, inventoryType, allowableClasses, armorSubClass
  
def blizzAPI(id):
  data = {}
  _blizz = json.load(urlopen('http://us.battle.net/api/wow/item/'+id))
  data['name'] = _blizz['name']
  if _blizz.get('weaponInfo'):
    data['weaponType'] = weaponSubClass[ str(_blizz['itemSubClass']) ]
  data['armorClass'] = _blizz['itemSubClass'] < len(armorSubClass) and armorSubClass[ _blizz['itemSubClass'] ] or ''
  data['icon'] = _blizz['icon']
  data['stats'] = [statmap.get( str(s['stat']) ) for s in _blizz['bonusStats'] if statmap.get( str(s['stat']) )]
  data['slot'] = inventoryType.get( str(_blizz['inventoryType']) )
  data['ilvl'] = _blizz['itemLevel']
  if _blizz.get('allowableClasses'):
    data['klass'] = allowableClasses[ _blizz['allowableClasses'][0] ]
  return data
    
class UpdateGear(form.SchemaForm):
  grok.name('update-gear')
  grok.require('cmf.ManagePortal')
  grok.context(IWoWResources)
  ignoreContext = True
  
  schema = IGearSchema
  
#  @button.buttonAndHandler(u'Import old gear')
#  def oldGear(self, action):
#    """ Temporary button to handle import """
#    from esoth.wow.content.gear import _gear
#    print len(_gear)
#    for item in _gear:
#      data = {'itemIds':[str(i) for i in item['ids']],
#              'source':item['boss']}
#      self.importItem(data)
#    IStatusMessage(self.request).addStatusMessage(_(u"Added items"),"info")
#    self.request.response.redirect(self.context.absolute_url()+'/@@gear-resources')
    
  def importItem(self, data):
    """ The work to import is done here, so multiple handlers can use it """
    gear = self.context.gear or []
    
    item_ids = set([])
    for id in data['itemIds']:
      if len(id.split(',')) > 1:
        item_ids.update(id.split(','))
      else:
        item_ids.add(id)
    
    item = {'ilvls':[],'agility':False,'strength':False,'intellect':False,'spirit':False,'dodge':False,'parry':False,'klass':''}
    item['source'] = data['source']
      
    # if we already have an entry, get rid of it (except for source) and add ids
    match = None
    for g in gear:
      if g['name'] == data.get('name'):
        match = g.copy()
        gear.remove(g)
    
    if match:
      item_ids.update(match['itemIds'])
      if not item['source']:
        item['source'] = match['source']
      
    item['itemIds'] = list(item_ids)
    
    for id in item_ids:
      # We have three sources 1) existing on portal, 2) form data, 3) blizz api
      blizz = blizzAPI(id)
      if data.get('name') and blizz['name'] != data['name']:
        IStatusMessage(self.request).addStatusMessage(_(u"%s does not match %s for id %s!!!" % (blizz['name'],item['name'],id)),"info")
        return self.request.response.redirect(self.context.absolute_url()+'/@@update-gear')
      if item.get('name') and blizz['name'] != item['name']:
        IStatusMessage(self.request).addStatusMessage(_(u"%s does not match %s for id %s!!!" % (blizz['name'],item['name'],id)),"info")
        return self.request.response.redirect(self.context.absolute_url()+'/@@update-gear')
      else:
        item['name'] = blizz['name']
      if not item.get('icon'):
        item['icon'] = blizz['icon']
      item['ilvls'].append(blizz['ilvl'])
      if not item.get('armorClass'):
        item['armorClass'] = blizz['armorClass']
      if not item.get('slot'):
        item['slot'] = blizz['slot']
      if blizz.get('klass'):
        item['klass'] = blizz['klass']
      for s in blizz['stats']:
        item[s] = True
      if blizz.get('weaponType') and not item.get('weaponType'):
        item['weaponType'] = blizz['weaponType']
    if not item.get('weaponType'):
      item['weaponType'] = ''
    gear.append(item)
    self.context.gear = gear
    return item['name']
  
  @button.buttonAndHandler(u'Update from Blizzard')
  def updateGear(self, action):
    data, errors = self.extractData()
    name = self.importItem(data)
    
    IStatusMessage(self.request).addStatusMessage(_(u"%s updated" % name),"info")
    self.request.response.redirect(self.context.absolute_url()+'/@@gear-resources')
  
  @button.buttonAndHandler(u'Add PTR/beta item')
  def updateGear(self, action):
    data, errors = self.extractData()
    gear = self.context.gear
    gear.append(data)
    self.context.gear = gear
    IStatusMessage(self.request).addStatusMessage(_(u"%s added" % item['name']),"info")
    self.request.response.redirect(self.context.absolute_url()+'/@@gear-resources')

class GearResourcesView(BrowserView):
  
  def gear(self):
    gear = self.context.gear
    gear.sort(lambda x,y: cmp(x['name'],y['name']))
    return gear

class ModGearResource(BrowserView):
  def __call__(self,name,dps_flag=False,healer_flag=False,tank_flag=False,agi=False,strength=False,intellect=False,b_start=''):
    gear = self.context.gear
    for g in gear:
      if g['name'] == name:
        item = g.copy()
        gear.remove(g)
        if dps_flag:
          item['dps_flag'] = True
        if healer_flag:
          item['healer_flag'] = True
        if tank_flag:
          item['dodge'] = True
          item['parry'] = True
        if agi:
          item['agility'] = True
        if strength:
          item['strength'] = True
        if intellect:
          item['intellect'] = True
        gear.append(item)
        self.context.gear=gear
        IStatusMessage(self.request).addStatusMessage(_(u"Updated"),"info")
        return self.request.response.redirect(self.context.absolute_url()+'/@@gear-resources?b_start='+b_start)
    IStatusMessage(self.request).addStatusMessage(_(u"Not found"),"warning")
    self.request.response.redirect(self.context.absolute_url()+'/@@gear-resources?b_start='+b_start)
    
class UpdateMounts(form.SchemaForm):
  grok.name('update-mounts')
  grok.require('cmf.ManagePortal')
  grok.context(IWoWResources)
  ignoreContext = True
  
  schema = IMountResourceSchema
  
#  @button.buttonAndHandler(u'Import old mount data')
#  def importOld(self, action):
#    mounts = []
#    path = os.path.dirname(os.path.realpath(__file__))
#    data = json.load(open(os.path.join(path,'..','mounts.json')))
#    for spellId, mount in data.items():
#      mount['spellId'] = spellId
#      mounts.append(mount)
#    self.context.mounts = mounts
#    IStatusMessage(self.request).addStatusMessage(_(u"%s updated" % mount.get('spellId') or mount.get('name')),"info")
#    self.request.response.redirect(self.context.absolute_url()+'/@@mount-resources')
  
  def importMount(self,data):
    mounts = self.context.mounts
    mount = {}
    if data.get('spellId'):
      match = {}
      for m in mounts:
        if m['spellId'] == data['spellId']:
          match = m.copy()
          mounts.remove(m)
      if match:
        for k,v in match.items():
          if v and v != '<NO_VALUE>':
            data[k]=v
    mount = {'spellId':data.get('spellId'),
             'name':data.get('name'),
             'restriction':data.get('restriction'),
             'icon':data.get('icon'),
             'faction':data.get('faction'),
             'isGround':data.get('isGround'),
             'isFlying':data.get('isFlying'),
             'isAquatic':data.get('isAquatic'),
             'isJumping':data.get('isJumping'),
             'obtainable':data.get('obtainable'),
             'location':data.get('location')}
    mounts.append(mount)
    self.context.mounts = mounts
    return mount.get('spellId') or mount.get('name')
  
  @button.buttonAndHandler(u'Update Mount')
  def updateMount(self, action):
    data, errors = self.extractData()
    name = self.importMount(data)
    
    IStatusMessage(self.request).addStatusMessage(_(u"%s updated" % name),"info")
    self.request.response.redirect(self.context.absolute_url()+'/@@mount-resources')

class MountResourcesView(BrowserView):
  
  def mounts(self):
    mounts = self.context.mounts or []
    mounts.sort(lambda x,y: cmp(x['name'],y['name']))
    return mounts


class ExportResources(BrowserView):
  def __call__(self):
    data = {'gear':self.context.gear,'pets':self.context.pets,'mounts':self.context.mounts}
    jsondata = json.dumps(data)
    
    self.request.response.setHeader('Content-type','application/json')
    self.request.response.setHeader('Content-Disposition', 'attachment; filename=resources.json')
    return jsondata

class ImportResources(BrowserView):
  """ """
  def __call__(self):
    path = os.path.dirname(os.path.realpath(__file__))
    f=open(os.path.join(path,'..','resources.json'))
    data=json.load(f); f.close()
    self.context.gear = data.get('gear')
    self.context.pets = data.get('pets')
    self.context.mounts = data.get('mounts')
    
class UpdatePets(form.SchemaForm):
  grok.name('update-pets')
  grok.require('cmf.ManagePortal')
  grok.context(IWoWResources)
  ignoreContext = True
  
  schema = IPetResourceSchema
  
#  @button.buttonAndHandler(u'Import old pets')
#  def oldPets(self, action):
#    """ Temporary button to handle import """
#    pets = []
#    path = os.path.dirname(os.path.realpath(__file__))
#    data = json.load(open(os.path.join(path,'..','pets.json')))
#    for speciesId, pet in data.items():
#      pet['speciesId'] = speciesId
#      pets.append(pet)
#    self.context.pets = pets
#    IStatusMessage(self.request).addStatusMessage(_(u"Pets updated"),"info")
#    self.request.response.redirect(self.context.absolute_url()+'/@@pet-resources')
  
  @button.buttonAndHandler(u'Update Pet')
  def updatePet(self, action):
    data, errors = self.extractData()
    pets = self.context.pets
    pet = {}
    name = data.get('name')
    match = {}
    if data.get('speciesId'):
      for p in pets:
        if p['speciesId'] == data['speciesId']:
          match = p.copy()
          pets.remove(p)
    match['speciesId'] = data.get('speciesId') or match.get('speciesId') or ''
    match['health'] = data.get('health') or match.get('health') or ''
    match['speed'] = data.get('speed') or match.get('speed') or ''
    match['power'] = data.get('power') or match.get('power') or ''
    pets.append(match)
    self.context.pets = pets
    
    IStatusMessage(self.request).addStatusMessage(_(u"%s updated" % data.get('speciesId')),"info")
    self.request.response.redirect(self.context.absolute_url()+'/@@pet-resources')

class PetResourcesView(BrowserView):
  
  def pets(self):
    pets = self.context.pets
    pets.sort(lambda x,y: cmp(x['speciesId'],y['speciesId']))
    return pets