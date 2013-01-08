from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
        
class FindPlayer(BrowserView):
  def servers(self):
    return ['Aegwynn','Aerie Peak','Agamaggan','Aggramar','Akama','Alexstrasza','Alleria','Altar of Storms','Alterac Mountains','Aman\'Thul','Andorhal','Anetheron','Antonidas',
            'Anub\'arak','Anvilmar','Arathor','Archimonde','Area 52','Argent Dawn','Arthas','Arygos','Auchindoun','Azgalor','Azjol-Nerub','Azralon','Azshara','Azuremyst',
            'Baelgun','Balnazzar','Barthilas','Black Dragonflight','Blackhand','Blackrock','Blackwater Raiders','Blackwing Lair','Blade\'s Edge','Bladefist','Bleeding Hollow',
            'Blood Furnace','Bloodhoof','Bloodscalp','Bonechewer','Borean Tundra','Boulderfist','Bronzebeard','Burning Blade','Burning Legion','Caelestrasz','Cairne','Cenarion Circle',
            'Cenarius','Cho\'gall','Chromaggus','Coilfang','Crushridge','Daggerspine','Dalaran','Dalvengyr','Dark Iron','Darkspear','Darrowmere','Dath\'Remar','Dawnbringer','Deathwing',
            'Demon Soul','Dentarg','Destromath','Dethecus','Detheroc','Doomhammer','Draenor','Dragonblight','Dragonmaw','Drak\'Tharon','Drak\'thul','Draka','Drakkari','Dreadmaul',
            'Drenden','Dunemaul','Durotan','Duskwood','Earthen Ring','Echo Isles','Eitrigg','Eldre\'Thalas','Elune','Emerald Dream','Eonar','Eredar','Executus','Exodar','Farstriders',
            'Feathermoon','Fenris','Firetree','Fizzcrank','Frostmane','Frostmourne','Frostwolf','Galakrond','Gallywix','Garithos','Garona','Garrosh','Ghostlands','Gilneas','Gnomeregan',
            'Goldrinn','Gorefiend','Gorgonnash','Greymane','Grizzly Hills','Gul\'dan','Gundrak','Gurubashi','Hakkar','Haomarush','Hellscream','Hydraxis','Hyjal','Icecrown','Illidan',
            'Jaedenar','Jubei\'Thos','Kael\'thas','Kalecgos','Kargath','Kel\'Thuzad','Khadgar','Khaz Modan','Khaz\'goroth','Kil\'jaeden','Kilrogg','Kirin Tor','Korgath','Korialstrasz',
            'Kul Tiras','Laughing Skull','Lethon','Lightbringer','Lightning\'s Blade','Lightninghoof','Llane','Lothar','Madoran','Maelstrom','Magtheridon','Maiev','Mal\'Ganis',
            'Malfurion','Malorne','Malygos','Mannoroth','Medivh','Misha','Mok\'Nathal','Moon Guard','Moonrunner','Mug\'thol','Muradin','Nagrand','Nathrezim','Nazgrel','Nazjatar',
            'Nemesis','Ner\'zhul','Nesingwary','Nordrassil','Norgannon','Onyxia','Perenolde','Proudmoore','Quel\'dorei','Quel\'Thalas','Ragnaros','Ravencrest','Ravenholdt','Rexxar',
            'Rivendare','Runetotem','Sargeras','Saurfang','Scarlet Crusade','Scilla','Sen\'jin','Sentinels','Shadow Council','Shadowmoon','Shadowsong','Shandris','Shattered Halls',
            'Shattered Hand','Shu\'halo','Silver Hand','Silvermoon','Sisters of Elune','Skullcrusher','Skywall','Smolderthorn','Spinebreaker','Spirestone','Staghelm',
            'Steamwheedle Cartel','Stonemaul','Stormrage','Stormreaver','Stormscale','Suramar','Tanaris','Terenas','Terokkar','Thaurissan','The Forgotten Coast','The Scryers',
            'The Underbog','The Venture Co','Thorium Brotherhood','Thrall','Thunderhorn','Thunderlord','Tichondrius','Tol Barad','Tortheldrin','Trollbane','Turalyon','Twisting Nether',
            'Uldaman','Uldum','Undermine','Ursin','Uther','Vashj','Vek\'nilash','Velen','Warsong','Whisperwind','Wildhammer','Windrunner','Winterhoof','Wyrmrest Accord','Ysera',
            'Ysondre','Zangarmarsh','Zul\'jin','Zuluhed']

  
  def __call__(self,character='',server=''):
    if character and server:
      catalog = getToolByName(self.context,'portal_catalog')
      character = character[0].upper() + character[1:].lower()
      _character = character.lower()
      server = server.replace("'",'')
      server = ' '.join([s[0].upper() + s[1:].lower() for s in server.split(' ')])
      _server = server.lower().replace("'","")
      results = catalog(portal_type='WoWChar',Title=character,server=server)
      
      if results:
        self.request.response.redirect(results[0].getURL())
      else:        
        # check if exists
        base_url = 'http://us.battle.net/api/wow/character/%s/%s?fields=guild,talents,stats,items,reputation,titles,professions,appearance,companions,mounts,pets,achievements,progression,titles'
        import json, urllib
        url = base_url % (_server,_character)
        _json = json.load(urllib.urlopen(url))
        if not _json.get('level'):
          self.request.set('errors','Not found')
        elif _json['level'] != 90:
          self.request.set('errors','Not max level')
        else:
          folder = self.context
          id = character.lower()
          count = 1
          if id in folder.objectIds():
            newid=id+'-%d' % count
            while newid in folder.objectIds():
              count+=1
              newid=id+'-%d' % count
            id = newid
          folder.invokeFactory('WoWChar',id)
          char=folder[id]
          char.setTitle(character)
          char.setServer(server)
          char.autoUpdateData()
          self.request.response.redirect(char.absolute_url())
    
    template = ZopeTwoPageTemplateFile('find_player.pt')
    return template(self)