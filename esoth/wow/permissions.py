from Products.CMFCore.permissions import setDefaultRoles

AddWoWChar='esoth.wow: Add WoW Char'
setDefaultRoles(AddWoWChar,('Anonymous','Authenticated'))

AddWoWDisplay='esoth.wow: Add WoW Display'
setDefaultRoles(AddWoWDisplay,('Manager','Owner'))

AddGearPath='esoth.wow: Add GearPath'
setDefaultRoles(AddGearPath,('Manager','Owner'))