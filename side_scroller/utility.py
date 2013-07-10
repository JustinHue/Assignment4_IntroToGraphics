'''
Created on Jun 14, 2013

@author: Justin Hellsten
'''
__CONFIG_DIR = ''
__CONFIG_MAP = {}
    
def init():
    __CONFIG_DIR = __open_config_file('config.cfg')
       
def get_config_value(key, default):
    if __CONFIG_DIR != '':
        value = __CONFIG_MAP.get(key)
        return value if value else default
    return default
    
def set_config_file(directory):
    global __CONFIG_DIR, __CONFIG_MAP
    __CONFIG_DIR = __open_config_file(directory)
    if __CONFIG_DIR != '':
        __CONFIG_MAP = __populate_map(open(__CONFIG_DIR, 'r'))

def get_config_path():
    return __CONFIG_DIR

def __open_config_file(directory):
    try:
        with open(directory): pass
        return directory        
    except IOError:
        return ''
    
def __populate_map(configFile):
    line, configMap = '', {}
    for line in configFile.readlines():
        tokens = line.strip().split('=')
        if len(tokens) == 2:
            configMap[tokens[0]] = tokens[1]  
    return configMap

