'''
Created on 26.02.2015

@summary: registry parsers
    @author: Simon Döbereiner
		@license: GPL v2
'''

from mimetypes import _winreg
from winreg import EnumKey
import re

REG_SECURITY = _winreg.KEY_WOW64_64KEY + _winreg.KEY_ALL_ACCESS

"""    
    @return: registry entries (key, type, value)    
    @param: full registry path 
    @description: parsing registry entries into a dictionary
"""         
def parse_by_path_single(filePath):
    registryEntries = {}
            
    try:
        location = _winreg.HKEY_LOCAL_MACHINE
        aReg = _winreg.ConnectRegistry(None, location)
        aKey = _winreg.OpenKey(aReg, filePath, 0, (REG_SECURITY))
        for i in range(_winreg.QueryInfoKey(aKey)[1]):
        
            name,value,rtype, = _winreg.EnumValue(aKey, i)
            registryEntries[name] = (value,rtype)
            
        _winreg.CloseKey(aKey)
        _winreg.CloseKey(aReg)
    
        return registryEntries
    except WindowsError:
        pass

                             
"""    
    @return: registry entries (key, type, value)    
    @param: Software name and optional a special folder 
    @description: saerching and parsing registry entries into a dictionary
"""         
def parseRegistry(software_name, special_folder = ''):
    registry_entries = {}
    rex = re.compile(software_name + '*', re.IGNORECASE) 
         
    try:
        registry_path = r'SOFTWARE\\' + special_folder
        aKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, (REG_SECURITY))
        
        #search whole registry for desired folder
        for i in range(_winreg.QueryInfoKey(aKey)[0]):
            folder = EnumKey(aKey,i)   
            target = rex.search(folder)
            #if found, read info of folder                
            if target:  
                _winreg.CloseKey(aKey)
#                 print(folder)
                temp_dict = parse_registry_single(folder)
#                 print(temp_dict)
                subKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path + '\\' + folder, 0, (REG_SECURITY))
                #look for subfolders and read them
                for k in range(_winreg.QueryInfoKey(subKey)[0]):
                    subfolder = EnumKey(subKey, k)
#                     print(subfolder)
                    temp_subdict = parse_registry_single(special_folder + '\\' + folder + '\\' + subfolder)                        
#                     print(temp_subdict)  
                    registry_entries = {subfolder : temp_subdict }                                         
                    print(registry_entries)  
                _winreg.CloseKey(subKey)
    except WindowsError as e:
#         print(e)
        pass
   
   
"""    
    @return: registry entries (key, type, value)  
    @param: subfolders
    @description: parsing registry entries into a dictionary
"""     
def parse_registry_single(registry_path):
    registry_entries = {}
    temp_subdict = {}
            
    try:
        location = _winreg.HKEY_LOCAL_MACHINE
        aReg = _winreg.ConnectRegistry(None, location)
        aKey = _winreg.OpenKey(aReg, r'SOFTWARE\\' + registry_path, 0, (REG_SECURITY))
        for i in range(_winreg.QueryInfoKey(aKey)[1]):        
            name,value,rtype, = _winreg.EnumValue(aKey, i)
            registry_entries[name] = (value,rtype)
#         print(registry_entries)
        _winreg.CloseKey(aKey)
        _winreg.CloseKey(aReg)
        
        subKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\' + registry_path, 0, (REG_SECURITY))
        #look for subfolders and read them
        for k in range(_winreg.QueryInfoKey(subKey)[0]):
            subfolder = EnumKey(subKey, k)
#             print(subfolder)
            temp_subdict = parse_registry_single(registry_path + '\\' + subfolder)
#             print(temp_subdict)                   
            registry_entries[subfolder] = temp_subdict
#         print(registry_entries)
        _winreg.CloseKey(subKey)
        return registry_entries
    except WindowsError as e:
#         print(e)
        pass