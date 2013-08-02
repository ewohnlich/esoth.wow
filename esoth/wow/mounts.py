from zope.interface import implements
from interfaces import IMountUtility
import json, os

import logging
logger = logging.getLogger("esoth.wow")

class MountUtility:
  implements(IMountUtility)
  
  def applyClasses(self, m, default_faction):
    klass = []
    faction = default_faction == 'Alliance' and 'A' or 'H'
    obtainable = 'Y'
    klass.append(m.get('isCollected') and 'obtainedMount' or 'unobtainedMount')
    klass.append(m.get('faction',faction).lower() == 'a' and 'allianceMount' or m['faction'] == 'H' and 'hordeMount' or 'bothMount')
    klass.append(m.get('obtainable',obtainable).lower() == 'y' and 'obtainableMount' or 'unobtainableMount')
    klass.append(' '.join([m.get(k) and k or 'not'+k for k in ('isJumping','isGround','isFlying','isAquatic',)]))
    m = m.copy()
    m['classes'] = ' '.join(klass)
    return m
  
  def mountData(self, mounts, default_faction):
    """ Combine json info on all mounts with collected mount info
    """
    data = json.load(open(os.path.join(os.path.dirname(__file__),'mounts.json')))
    _mounts = []
    _flag = False
    for id,info in data.items():
      _mount = {'icon':info.get('icon'),
                'isCollected':info.get('isCollected'),
                'isGround':info.get('isGround'),
                'isFlying':info.get('isFlying'),
                'isAquatic':info.get('isAquatic'),
                'isJumping':info.get('isJumping'),
                'spellId':id,
                'name':info['name'],
                'location':info['location'],
                'obtainable':info['obtainable'],
                'faction':info['faction']}
      mkeys = mounts.keys()
      mkeys.sort()
        
      if id in mounts:
        if mounts[id]['name'] != info['name']:
          logger.warn('%s (import) vs %s (blizz)' % (info['name'],mounts[id]['name']))
        if info['location'] == 'unknown':
          logger.warn('unknown location - %s' % info['name'])
        if info['faction'] == 'U':
          logger.warn('unknown faction - %s' % info['name'])
        if info['obtainable'] == 'U':
          logger.warn('unknown if obtainable - %s' % info['obtainable'])
        _mount.update({'isCollected':True,
                       'icon':mounts[id]['icon'],
                       'name':mounts[id]['name'],
                       'itemId':mounts[id]['itemId'],
                       'isGround':mounts[id]['isGround'],
                       'isFlying':mounts[id]['isFlying'],
                       'isAquatic':mounts[id]['isAquatic'],
                       'isJumping':mounts[id]['isJumping']})
        if not data[id].get('icon'):
          data[id]['icon'] = mounts[id]['icon']
          data[id]['isGround'] = mounts[id]['isGround']
          data[id]['isFlying'] = mounts[id]['isFlying']
          data[id]['isAquatic'] = mounts[id]['isAquatic']
          data[id]['isJumping'] = mounts[id]['isJumping']
          logger.info('added icon and statuses for %s' % str(id))
          _flag = True
        
      _mounts.append(self.applyClasses(_mount,default_faction))
    for id in mounts.keys():
      # we don't have any data on this one
      if id not in data:
        _flag = True
        logger.warn('added - %s' % info['name'])
        data[id] = {'name':mounts[id]['name'],'faction':'U','obtainable':'U','location':'unknown'}
        _mounts.append(self.applyClasses({'isCollected':True,
                        'icon':mounts[id]['icon'],
                        'location':'unknown',
                        'faction':'U',
                        'obtainable':'U',
                        'spellId':id,
                        'itemId':mounts[id]['itemId'],
                        'name':mounts[id]['name'],
                        'isGround':mounts[id]['isGround'],
                        'isFlying':mounts[id]['isFlying'],
                        'isAquatic':mounts[id]['isAquatic'],
                        'isJumping':mounts[id]['isJumping']},default_faction))
                   
    if _flag:
      json.dump(data,open(os.path.join(os.path.dirname(__file__),'mounts.json'),'w'))       
    return _mounts