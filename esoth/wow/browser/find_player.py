from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from urllib import urlopen
import json
        
class FindPlayer(BrowserView):
  def servers(self):
    try:
      realms = json.load(urlopen('http://us.battle.net/api/wow/realm/status'))['realms']
    except:
      realms = json.load(urlopen('http://www.esoth.com/proxyw?u=http://us.battle.net/api/wow/realm/status'))['realms']
    return [{'id':r['slug'], 'title':'%s (US)' % r['name']} for r in realms]

  
  def __call__(self,character='',server=''):
    if character and server:
      catalog = getToolByName(self.context,'portal_catalog')
      results = catalog(object_provides='esoth.wow.content.gearpath.IGearPath',Title=character,server=server)
      
      if results:
        self.request.response.redirect(results[0].getURL())
      else:
        
        #check exists
        base_url = 'http://us.battle.net/api/wow/character/%s/%s?fields=guild,talents,stats,items,reputation,titles,professions,appearance,companions,mounts,pets,achievements,progression,titles'
        url = base_url % (server,character)
        try:
          data = json.load(urlopen(url))
        except ValueError:
          data = json.load(urlopen('http://www.esoth.com/proxyw?u='+url))
        if not data.get('level'):
          self.request.set('errors','Not found')
        
        folder = self.context
        id = character.lower()
        count = 1
        if id in folder.objectIds():
          newid=id+'-%d' % count
          while newid in folder.objectIds():
            count+=1
            newid=id+'-%d' % count
          id = newid
        folder.invokeFactory('GearPath',id)
        char=folder[id]
        char.title = character
        char.server = server
        ob = folder[id]
        ob.autoUpdateData()
        self.request.response.redirect(ob.absolute_url())
    
    template = ZopeTwoPageTemplateFile('find_player.pt')
    return template(self)