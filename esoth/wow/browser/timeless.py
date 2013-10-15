from five import grok
from plone.directives import form
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile, ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from urllib import urlopen
import json

gnabb = [
{'name':'Cursed Swabby Helmet',
  'source':'Sunken Treasure',
  'rare':True,
  'pet':False,
  'location':'Shipwreck south of Old Pi\'jiu - weekly',
  'alternative':'',
  'id':104038,
  'source_url':'http://www.wowhead.com/object=220832',
  'icon':'inv_helmet_49'},
{'name':'Warped Warning Sign',
  'source':'Ordon Oathguards',
  'rare':False,
  'pet':False,
  'location':'Firewalker Ruins',
  'alternative':'',
  'id':104330,
  'source_url':'http://www.wowhead.com/npc=72892',
  'icon':'trade_archaeology_vrykul_runestick'},
{'name':'Giant Purse of Timeless Coins',
  'source':'Karkanos',
  'rare':True,
  'pet':False,
  'location':'Fishing dock on the south, central coast.',
  'alternative':'',
  'id':104035,
  'source_url':'http://www.wowhead.com/npc=72193',
  'icon':'inv_misc_bag_09'},
{'name':'Crystal of Insanity',
  'source':'Eerie Crystal',
  'rare':False,
  'pet':False,
  'location':'Cavern of Lost Spirits. These are the purple containers throughout the cave',
  'alternative':'Sulik\'shor - rare in Valley of the Four Winds',
  'id':86569,
  'source_url':'http://www.wowhead.com/object=222686',
  'icon':'inv_enchant_voidcrystal'},
{'name':'Battle Horn',
  'source':'Ordon Candlekeeper',
  'rare':False,
  'pet':False,
  'location':'Firewalker Ruins',
  'alternative':'Blackhoof - rare in Valley of the Four Winds',
  'id':86565,
  'source_url':'http://www.wowhead.com/npc=72875',
  'icon':'inv_misc_horn_01'},
{'name':'Elixir of Ancient Knowledge',
  'source':'Archiereus of Flame',
  'rare':True,
  'pet':False,
  'location':'Ordon Sanctuary (cloak area), also summonable north of the court with a vendor item',
  'alternative':'Krol the Blade, rare in Dread Wastes along the wall',
  'id':86574,
  'source_url':'http://www.wowhead.com/npc=73174',
  'icon':'inv_alchemy_potion_04'},
{'name':'Forager\'s Gloves',
  'source':'Burning Berserkers',
  'rare':False,
  'pet':False,
  'location':'The Blazing Way',
  'alternative':'Korda Torros, rare in Kun-Lai Summit',
  'id':86566,
  'source_url':'http://www.wowhead.com/npc=72895',
  'icon':'inv_glove_pvpwarlock_e_01'},
{'name':'Big Bag of Herbs',
  'source':'Ashleaf Sprites or Burning Berserkers',
  'rare':False,
  'pet':False,
  'location':'The Blazing Way',
  'alternative':'',
  'id':106130,
  'source_url':'http://www.wowhead.com/npc=72877',
  'icon':'achievement_guildperk_bountifulbags'},
{'name':'Overgrown Lilypad',
  'source':'Gulp Frogs',
  'rare':False,
  'pet':False,
  'location':'East coast of the island',
  'alternative':'Sel\'ena, rare in Valley of the Four Winds',
  'id':86580,
  'source_url':'http://www.wowhead.com/npc=72777',
  'icon':'inv_relics_idolofhealth'},
{'name':'Hardened Shell',
  'source':'Great Turtle Furyshell or Chelon',
  'rare':False,
  'pet':False,
  'location':'West coast, former is mid-south, latter is north',
  'alternative':'Nessos the Oracle, rare in northern Kun-Lai Summit',
  'id':86584,
  'source_url':'http://www.wowhead.com/npc=73161',
  'icon':'inv_shield_18'},
{'name':'Bubbling Pi\'jiu Brew',
  'source':'Spectral Windwalkers',
  'rare':False,
  'pet':False,
  'location':'Old Pi\'jiu',
  'alternative':'',
  'id':104336,
  'source_url':'http://www.wowhead.com/npc=73021',
  'icon':'spell_monk_nimblebrew'},
{'name':'Thick Pi\'jiu Brew',
  'source':'Spectral Brewmasters',
  'rare':False,
  'pet':False,
  'location':'Old Pi\'jiu',
  'alternative':'',
  'id':104335,
  'source_url':'http://www.wowhead.com/npc=73018',
  'icon':'achievement_faction_brewmaster'},
{'name':'Misty Pi\'jiu Brew',
  'source':'Spectral Mistweavers',
  'rare':False,
  'pet':False,
  'location':'Old Pi\'jiu',
  'alternative':'',
  'id':104334,
  'source_url':'http://www.wowhead.com/npc=73025',
  'icon':'ability_monk_chibrew'},
{'name':'Warning Sign',
  'source':'Jakur of Ordon',
  'rare':True,
  'pet':False,
  'location':'Firewalker Ruins',
  'alternative':'',
  'id':104331,
  'source_url':'http://www.wowhead.com/npc=73169',
  'icon':'trade_archaeology_vrykul_runestick'},
{'name':'Ash-Covered Horn',
  'source':'Flintlord Gairan or High Priest of Ordos',
  'rare':True,
  'pet':False,
  'location':'Ordon Sanctuary',
  'alternative':'',
  'id':104329,
  'source_url':'http://www.wowhead.com/npc=73172',
  'icon':'inv_misc_monsterhorn_02'},
{'name':'Cauterizing Core',
  'source':'Molten Guardians',
  'rare':False,
  'pet':False,
  'location':'Ordon Sanctuary and the bridge just before it',
  'alternative':'Cinderfall',
  'id':104328,
  'source_url':'http://www.wowhead.com/npc=72888',
  'icon':'inv_summerfest_firespirit'},
{'name':'Captain Zvezdan\'s Lost Leg',
  'source':'Rattleskew',
  'rare':True,
  'pet':False,
  'location':'South-east of the coast, at a sunken boat',
  'alternative':'',
  'id':104321,
  'source_url':'http://www.wowhead.com/npc=72048',
  'icon':'inv_mace_11'},
{'name':'Cursed Talisman',
  'source':'Spelurk',
  'rare':True,
  'pet':False,
  'location':'Cave-in event, just to the east of the court',
  'alternative':'',
  'id':104320,
  'source_url':'http://www.wowhead.com/npc=71864',
  'icon':'inv_jewelry_necklace_55'},
{'name':'Golden Moss',
  'source':'Rock Moss',
  'rare':True,
  'pet':False,
  'location':'Cavern of Lost Souls',
  'alternative':'',
  'id':104313,
  'source_url':'http://www.wowhead.com/npc=73157',
  'icon':'inv_misc_necklacea6'},
{'name':'Strange Glowing Mushroom',
  'source':'Damp Shamblers',
  'rare':False,
  'pet':False,
  'location':'Cavern of Lost Souls',
  'alternative':'Rock Moss',
  'id':104312,
  'source_url':'http://www.wowhead.com/npc=72771',
  'icon':'spell_druid_wildmushroom_bloom'},
{'name':'Eternal Kiln',
  'source':'Eternal Kilnmasters',
  'rare':False,
  'pet':False,
  'location':'The Blazing Way and Ordon Sanctuary',
  'alternative':'',
  'id':104309,
  'source_url':'http://www.wowhead.com/npc=72896',
  'icon':'inv_summerfest_firedrink'},
{'name':'Jadefire Spirit',
  'source':'Spirit of Jadefire',
  'rare':True,
  'pet':True,
  'location':'Cavern of Lost Souls',
  'alternative':'',
  'id':104307,
  'source_url':'http://www.wowhead.com/npc=72769',
  'icon':'spell_fire_felfire'},
{'name':'Sunset Stone',
  'source':'Urdur the Cauterizer',
  'rare':True,
  'pet':False,
  'location':'Ordon Sanctuary (cloak area)',
  'alternative':'',
  'id':104306,
  'source_url':'http://www.wowhead.com/npc=73173',
  'icon':'inv_elemental_eternal_life'},
{'name':'Ashen Stone',
  'source':'Watcher Osu',
  'rare':True,
  'pet':False,
  'location':'Firewalker Ruins',
  'alternative':'',
  'id':104305,
  'source_url':'http://www.wowhead.com/npc=73170',
  'icon':'inv_elemental_eternal_fire'},
{'name':'Blizzard Stone',
  'source':'Blazebound Chanters',
  'rare':False,
  'pet':False,
  'location':'The Blazing Way and Ordon Sanctuary',
  'alternative':'',
  'id':104304,
  'source_url':'http://www.wowhead.com/npc=72897',
  'icon':'inv_elemental_eternal_air'},
{'name':'Rain Stone',
  'source':'Zesqua',
  'rare':True,
  'pet':False,
  'location':'South, central off the coast',
  'alternative':'',
  'id':104303,
  'source_url':'http://www.wowhead.com/npc=72245',
  'icon':'inv_elemental_eternal_water'},
{'name':'Blackflame Daggers',
  'source':'Champion of the Black Flame',
  'rare':True,
  'pet':False,
  'location':'Paths around The Blazing Way',
  'alternative':'',
  'id':104302,
  'source_url':'http://www.wowhead.com/npc=73171',
  'icon':'inv_knife_1h_grimbatolraid_d_03'},
{'name':'Falling Flame',
  'source':'Cinderfall',
  'rare':True,
  'pet':False,
  'location':'The bridge leading to the cloak area',
  'alternative':'',
  'id':104299,
  'source_url':'http://www.wowhead.com/npc=73175',
  'icon':'spell_fire_meteorstorm'},
{'name':'Ordon Death Chime',
  'source':'Flintlord Gairan',
  'rare':True,
  'pet':False,
  'location':'Ordon Sanctuary (cloak area)',
  'alternative':'',
  'id':104298,
  'source_url':'http://www.wowhead.com/npc=73172',
  'icon':'inv_misc_necklace_firelands_2'},
{'name':'Blazing Sigil of Ordos',
  'source':'Ordon Fire-Watchers',
  'rare':False,
  'pet':False,
  'location':'Firewalker Ruins',
  'alternative':'Eternal Kilnmasters, those these aren\'t as efficient to farm',
  'id':104297,
  'source_url':'http://www.wowhead.com/npc=72894',
  'icon':'spell_fire_rune'},
{'name':'Ordon Ceremonial Robes',
  'source':'Ordon Fire-Watchers',
  'rare':False,
  'pet':False,
  'location':'Firewalker Ruins',
  'alternative':'Also Blazebound Chanters, Watcher Osu, and Urdur the Cauterizer',
  'id':104296,
  'source_url':'http://www.wowhead.com/npc=72894',
  'icon':'inv_chest_robe_raidmage_j_01'},
{'name':'Rime of the Time-Lost Mariner',
  'source':'Dread Ship Vezuvius',
  'rare':True,
  'pet':False,
  'location':'Northwest, off the coast.',
  'alternative':'',
  'id':104294,
  'source_url':'http://www.wowhead.com/npc=73281',
  'icon':'spell_warlock_soulburn'},
{'name':'Scuttler\'s Shell',
  'source':'Ancient Spineclaw',
  'rare':False,
  'pet':False,
  'location':'All around the island, off the coasts',
  'alternative':'Monstrous Spineclaw',
  'id':104293,
  'source_url':'http://www.wowhead.com/npc=72841',
  'icon':'inv_misc_coin_14'},
{'name':'Partially-Digested Meal',
  'source':'Death Adders',
  'rare':False,
  'pet':False,
  'location':'West side of the island',
  'alternative':'Imperial Python',
  'id':104292,
  'source_url':'http://www.wowhead.com/npc=72841',
  'icon':'inv_misc_food_84_roastclefthoof'},
{'name':'Swarmling of Gu\'chi',
  'source':'Gu\'chi the Swarmbringer',
  'rare':True,
  'pet':True,
  'location':'Just east of Old Pi\'jiu',
  'alternative':'',
  'id':104291,
  'source_url':'http://www.wowhead.com/npc=72909',
  'icon':'inv_misc_food_vendor_boiledsilkwormpupa'},
{'name':'Sticky Silkworm Goo',
  'source':'Spotted Swarmers',
  'rare':False,
  'pet':False,
  'location':'Near Old Pi\'jiu',
  'alternative':'Gu\'chi the Swarmbringer',
  'id':104290,
  'source_url':'http://www.wowhead.com/npc=72908',
  'icon':'inv_misc_web_01'},
{'name':'Faintly-Glowing Herb',
  'source':'Ashleaf Sprites',
  'rare':False,
  'pet':False,
  'location':'The Blazing Way',
  'alternative':'Leafmender',
  'id':104289,
  'source_url':'http://www.wowhead.com/npc=72877',
  'icon':'spell_lfieblood'},
{'name':'Condensed Jademist',
  'source':'Jademist Dancers',
  'rare':False,
  'pet':False,
  'location':'Northwest coast',
  'alternative':'',
  'id':104288,
  'source_url':'http://www.wowhead.com/npc=72767',
  'icon':'ability_monk_renewingmists'},
{'name':'Windfeather Plume',
  'source':'Brilliant Windfeathers',
  'rare':False,
  'pet':False,
  'location':'West and south side of the island',
  'alternative':'Emerald Gander',
  'id':104287,
  'source_url':'http://www.wowhead.com/npc=72762',
  'icon':'ability_priest_angelicfeather'},
{'name':'Quivering Firestorm Egg',
  'source':'Crimsonscale Firestorm',
  'rare':False,
  'pet':False,
  'location':'The Blazing Way',
  'alternative':'Huolon',
  'id':104286,
  'source_url':'http://www.wowhead.com/npc=72867',
  'icon':'inv_cloudserpent_egg_red'},
{'name':'Reins of the Thundering Onyx Cloud Serpent',
  'source':'Huolon',
  'rare':True,
  'pet':False,
  'location':'The Blazing Way, just after the first bridge',
  'alternative':'',
  'id':104269,
  'source_url':'http://www.wowhead.com/npc=73167',
  'icon':'inv_pandarenserpentmount_lightning_black'},
{'name':'Pristine Stalker Hide',
  'source':'Primal Stalkers',
  'rare':False,
  'pet':False,
  'location':'East of the central court',
  'alternative':'Cranegnasher and Tsavo\'ka',
  'id':104268,
  'source_url':'http://www.wowhead.com/npc=72805',
  'icon':'inv_misc_pelt_14'},
{'name':'Glinting Pile of Stone',
  'source':'Eroded Cliffdwellers',
  'rare':False,
  'pet':False,
  'location':'East of the central court',
  'alternative':'Golganarr',
  'id':104263,
  'source_url':'http://www.wowhead.com/npc=72809',
  'icon':'inv_jewelcrafting_livingruby_02'},
{'name':'Odd Polished Stone',
  'source':'Eroded Pile of Stone',
  'rare':False,
  'pet':False,
  'location':'East of the central court',
  'alternative':'Golganarr',
  'id':104262,
  'source_url':'http://www.wowhead.com/npc=72809',
  'icon':'inv_misc_enchantedpearld'},
{'name':'Glowing Blue Ash',
  'source':'Foreboding Flames',
  'rare':False,
  'pet':False,
  'location':'Cavern of Lost Souls',
  'alternative':'Cinderfall',
  'id':104261,
  'source_url':'http://www.wowhead.com/npc=73162',
  'icon':'inv_misc_powder_adamantite'},
{'name':'Glowing Green Ash',
  'source':'Spirit of Jadefire',
  'rare':True,
  'pet':False,
  'location':'Cavern of Lost Souls',
  'alternative':'',
  'id':104258,
  'source_url':'http://www.wowhead.com/npc=72769',
  'icon':'inv_misc_powder_feliron'},
{'name':'Bonkers',
  'source':'Loot from Master Kukuru\'s Chest',
  'rare':False,
  'pet':True,
  'location':'The chest key vendor and chests are in a cave to the east of Mossgreen Lake',
  'alternative':'',
  'id':104202,
  'source_url':'http://www.wowhead.com/npc=72007',
  'icon':'inv_pet_monkey'},
{'name':'Gulp Froglet',
  'source':'Bufo',
  'rare':True,
  'pet':True,
  'location':'East coast',
  'alternative':'',
  'id':104169,
  'source_url':'http://www.wowhead.com/npc=72775',
  'icon':'inv_pet_toad_black'},
{'name':'Spineclaw Crab',
  'source':'Monstrous Spineclaw',
  'rare':True,
  'pet':True,
  'location':'Spawns in place of an Ancient Spineclaw, anywhere along the coast',
  'alternative':'',
  'id':104168,
  'source_url':'http://www.wowhead.com/npc=73166',
  'icon':'ability_hunter_pet_crab'},
{'name':'Skunky Alemental',
  'source':'Zhu-Gon the Sour',
  'rare':True,
  'pet':True,
  'location':'Skunky Ale event in Old Pi\'jiu',
  'alternative':'',
  'id':104167,
  'source_url':'http://www.wowhead.com/npc=71919',
  'icon':'inv_pet_pandarenelemental_earth'},
{'name':'Ominous Flame',
  'source':'Foreboding Flame',
  'rare':False,
  'pet':True,
  'location':'Cavern of Lost Souls',
  'alternative':'',
  'id':104166,
  'source_url':'http://www.wowhead.com/npc=73162',
  'icon':'spell_fire_bluefire'},
{'name':'Jademist Dancer',
  'source':'Jademist Dancer',
  'rare':False,
  'pet':True,
  'location':'Northwest coast',
  'alternative':'',
  'id':104164,
  'source_url':'http://www.wowhead.com/npc=72767',
  'icon':'inv_pet_pandarenelemental_air'},
{'name':'Death Adder Hatchling',
  'source':'Imperial Python',
  'rare':True,
  'pet':True,
  'location':'Around the west side of the island',
  'alternative':'',
  'id':104161,
  'source_url':'http://www.wowhead.com/npc=73163',
  'icon':'inv_pet_pythonbrown'},
{'name':'Dandelion Frolicker',
  'source':'Scary Sprite',
  'rare':True,
  'pet':True,
  'location':'Event at the Neverending Spritewood event, just south west of the Mossgreen Pond',
  'alternative':'',
  'id':104160,
  'source_url':'http://www.wowhead.com/npc=71862',
  'icon':'spell_nature_naturetouchgrow'},
{'name':'Ruby Droplet',
  'source':'Garnia',
  'rare':True,
  'pet':True,
  'location':'Red pool in the northwest. Requires an Albatross taxi',
  'alternative':'',
  'id':104159,
  'source_url':'http://www.wowhead.com/npc=73282',
  'icon':'inv_pet_pandarenelementa_fire'},
{'name':'Azure Crane Chick',
  'source':'Crane Nests',
  'rare':False,
  'pet':True,
  'location':'Crane nests are all over the west die of the island where cranes are',
  'alternative':'',
  'id':104157,
  'source_url':'http://www.wowhead.com/object=222685',
  'icon':'inv_pet_babycrane'},
{'name':'Ashleaf Spriteling',
  'source':'Leafmender',
  'rare':True,
  'pet':True,
  'location':'The Blazing Way',
  'alternative':'',
  'id':104156,
  'source_url':'http://www.wowhead.com/npc=73277',
  'icon':'spell_nature_dryaddispelmagic'},
]

class GnabbView(BrowserView):
  gnabb = gnabb
  
  def progress(self):
    _progress = self.request.get('s','')
    # it's hex, convert to binary
    if _progress:
      _progress = bin(int(_progress, 16))[2:]
    for i in range(0,len(_progress)):
      try:
        if int(_progress[i]):
          self.gnabb[i]['completed'] = True
        else:
          self.gnabb[i]['completed'] = False
      except IndexError: # you fucked up
        return []
    return self.gnabb
    
  def completed(self):
    return [g['id'] for g in self.gnabb if g.get('completed')]