#!/usr/bin/env python3

###########################
# Addon moduel maker tool #
# ======================= #
__version__ = 0.1

import os
import sys

PARAMS = sys.argv
PREFIX = ""
AUTHOR = ""
AUTHORS = ""
URL = ""


def getModData(file,string):
    try:
        os.stat('addons\\main\\{}'.format(file))
    except:
        sys.exit('{} could not be found...'.format(file))

    fileObject = open('addons\\main\\{}'.format(file), "r")
    for l in fileObject:
        if (string in l):
            data = l
    fileObject.close()
    return data

def cbaRequired():
    cbaIsRequired = False
    try:
        os.stat('addons\\main\\script_macros.hpp')
        #print('script_mod.hpp file detected')
    except:
        sys.exit('script_macros.hpp could not be found... \nCan\'t be determined if cba is pressent in MOD.')

    script_macros = open('addons\\main\\script_macros.hpp', "r")
    for l in script_macros:
        if ('\\x\\cba\\addons\\' in l):
            cbaIsRequired = True
    if cbaIsRequired == True:
        print('CBA is used in mod.')
    else:
        print('CBA not used in mod.')
    script_macros.close()
    return cbaIsRequired



def checkAddonExist(ADDON):
     for a in os.listdir('addons\\'):
         if ADDON in a:
             sys.exit('Addon {} already exist...'.format(ADDON))



def setUpNewAddon(ADDON,PREFIX,CBA,AUTHOR,AUTHORS,URL):
    print('Generating new addon {} for {}...'.format(ADDON,PREFIX))
    try:
        os.mkdir('addons\\{}'.format(ADDON))
    except:
        sys.exit('Fatal error could not create addon...')



    # set up $PBOPREFIX$
    try:
        object = '$PBOPREFIX$'
        addonfile = open('addons\\{}\\$PBOPREFIX$'.format(ADDON,object),"w+t")
    except:
        sys.exit('Fatal error could not create file...')
    print('Creating {}'.format(object))
    try:
        addonfile.write('z\\{}\\addons\\{}'.format(PREFIX,ADDON))
    except:
        sys.exit('Fatal error could not write to file...')
    addonfile.close()
    print('{} is created.'.format(object))



    # set up config.cpp
    try:
        object = 'config.cpp'
        addonfile = open('addons\\{}\\{}'.format(ADDON,object),"w+t")
    except:
        sys.exit('Fatal error could not create file...')
    print('Creating {}'.format(object))
    try:
        addonfile.write('#include "script_component.hpp"\n')
        addonfile.write('\n')
        addonfile.write('class CfgPatches {\n')
        addonfile.write('    class ADDON {\n')
        addonfile.write('        name = COMPONENT_NAME;\n')
        addonfile.write('        units[] = {};\n')
        addonfile.write('        weapons[] = {};\n')
        addonfile.write('        requiredVersion = REQUIRED_VERSION;\n')
        addonfile.write('        requiredAddons[] = {{\"{0}_main\",\"{0}_common\"}};\n'.format(PREFIX))
        addonfile.write('        author = {};\n'.format(AUTHOR))
        addonfile.write('        authors[] = {{{}}};\n'.format(AUTHORS))
        addonfile.write('        url = {};\n'.format(URL))
        addonfile.write('        VERSION_CONFIG;\n')
        addonfile.write('    };\n')
        addonfile.write('};\n')
    except:
        sys.exit('Fatal error could not write to file...')
    addonfile.close()
    print('{} is created.'.format(object))

    try:
        object = 'script_component.hpp'
        addonfile = open('addons\\{}\\{}'.format(ADDON,object),"w+t")
    except:
        sys.exit('Fatal error could not create file...')
    print('Creating {}'.format(object))
    try:
        addonfile.write('#define COMPONENT {}\n'.format(ADDON))
        addonfile.write('#define COMPONENT_BEAUTIFIED {}\n'.format(ADDON.title()))
        addonfile.write('\n')
        addonfile.write('#include \"\\z\\{}\\addons\\{}\\script_mod.hpp\"\n'.format(PREFIX,ADDON))
        addonfile.write('#include \"\\z\\{}\\addons\\{}\\script_macros.hpp\"\n'.format(PREFIX,ADDON))
    except:
        sys.exit('Fatal error could not write to file...')
    addonfile.close()
    print('{} is created.'.format(object))



def main():
    print("""
\033[1mAddon moduel maker tool v{}\033[0m
\033[90mThis tool creates a new addon for with given name.\033[0m
    """.format(__version__))

    # check params
    if len(PARAMS) <= 1:
        sys.exit("""
Atleast one parameter is required...
{} [ADDON]""".format(PARAMS[0]))
    try:
        ADDON = PARAMS[1]
    except:
        sys.exit('Addon can not be determined')


    # Getting project path
    scriptpath = os.path.realpath(__file__)
    projectpath = os.path.dirname(os.path.dirname(scriptpath))

    addonsfolder = 'addons'
    addonsPath = projectpath + '\\' + addonsfolder

    os.chdir(projectpath)

    # Create addons folder if none found
    try:
        os.stat(addonsfolder)
        print('Addons folder detected.')
    except:
        sys.exit('No addons folder detected...') # to do set up new project if none exist.

    # blacklisted addons
    if ('main' in PARAMS) or ('common' in PARAMS):
        sys.exit('Attempt is made to create a invalid addon...\nThis is not a valid addon name cause it should or are already present...'.format())

    # get mod name
    print('Checking for mod data...')
    PREFIX = getModData('script_mod.hpp','#define PREFIX')
    PREFIX = PREFIX[15:]
    PREFIX = PREFIX.rstrip()
    print('Mod prefix detected: {}.'.format(PREFIX))

    AUTHOR = getModData('config.cpp','author = ')
    AUTHOR = AUTHOR[17:]
    AUTHOR = AUTHOR[:-2]
    AUTHOR = AUTHOR.rstrip()
    print('Mod author detected: {}.'.format(AUTHOR))

    AUTHORS = getModData('config.cpp','authors[] = {')
    AUTHORS = AUTHORS[21:]
    AUTHORS = AUTHORS[:-3]
    AUTHORS = AUTHORS.rstrip()
    print('Mod authors detected: {}.'.format(AUTHORS))

    URL = getModData('config.cpp','url = ')
    URL = URL[14:]
    URL = URL[:-2]
    URL = URL.rstrip()
    print('Mod url detected: {}.'.format(URL))

    # check if CBA is used
    CBA = cbaRequired()


    checkAddonExist(ADDON)
    setUpNewAddon(ADDON,PREFIX,CBA,AUTHOR,AUTHORS,URL)


if __name__ == "__main__":
    sys.exit(main())
