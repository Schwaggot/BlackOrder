#!/usr/bin/env python3

###############
# Addon maker #
# =========== #
# This is a tool written to easy make new addonts. Free to use.
# Written by: Andreas Brostrom | Evul <andreas.brostrom.ce@gmail.com>

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
            modData = l
    fileObject.close()
    return modData


def findFile(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



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



def setUpNewAddon(ADDON,PREFIX,CBA,STRINGTABLE,AUTHOR,AUTHORS,URL):
    def buildFile(object,line):
        try:
            addonfile = open('addons\\{}\\{}'.format(ADDON,object),"w+t")
        except:
            sys.exit('Fatal error could not create file...')
        print('Creating {}'.format(object))
        try:
            for str in line:
                addonfile.write('{}\n'.format(str))
        except:
            sys.exit('Fatal error could not write to file...')
        addonfile.close()
        print('{} is created.'.format(object))


    print('Generating new addon {} for {}...'.format(ADDON,PREFIX))
    try:
        os.mkdir('addons\\{}'.format(ADDON))
    except:
        sys.exit('Fatal error could not create addon...')



    # build $PBOPREFIX$
    stringArray = ['z\\{}\\addons\\{}'.format(PREFIX,ADDON)]
    buildFile('$PBOPREFIX$',stringArray)

    # build config.cpp
    stringArray = [
        '#include "script_component.hpp"',
        '',
        'class CfgPatches {',
        '    class ADDON {',
        '        name = COMPONENT_NAME;',
        '        units[] = {};',
        '        weapons[] = {};',
        '        requiredVersion = REQUIRED_VERSION;',
        '        requiredAddons[] = {{\"{0}_main\",\"{0}_common\"}};'.format(PREFIX),
        '        author = {};'.format(AUTHOR),
        '        authors[] = {{{}}};'.format(AUTHORS),
        '        url = {};'.format(URL),
        '        VERSION_CONFIG;',
        '    };',
        '};'
    ]
    buildFile('config.cpp',stringArray)

    # build script_component.hpp
    if CBA:
        stringArray = [
            '#define COMPONENT {}'.format(ADDON),
            '#define COMPONENT_BEAUTIFIED {}'.format(ADDON.title()),
            '',
            '#include \"\\z\\{}\\addons\\{}\\script_mod.hpp\"'.format(PREFIX,ADDON),
            '#include \"\\z\\{}\\addons\\{}\\script_macros.hpp\"\n'.format(PREFIX,ADDON)
        ]
        buildFile('script_component.hpp',stringArray)


    #build stringtable.xml
    if STRINGTABLE:
        stringArray = [
            '<Project name="{}">'.format(PREFIX.title()),
            '    <Package name="{}">'.format(ADDON),
            '    </Package>',
            '</Project>'
        ]
        buildFile('stringtable.xml',stringArray)




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
    try:
        PREFIX = getModData('script_mod.hpp','PREFIX')
        PREFIX = PREFIX[15:]
        PREFIX = PREFIX.rstrip()
        print('Mod prefix detected: {}.'.format(PREFIX))
    except:
        PREFIX =''

    try:
        AUTHOR = getModData('config.cpp','author')
        AUTHOR = AUTHOR[17:]
        AUTHOR = AUTHOR[:-2]
        AUTHOR = AUTHOR.rstrip()
        print('Mod author detected: {}.'.format(AUTHOR))
    except:
        AUTHOR =''

    try:
        AUTHORS = getModData('config.cpp','authors')
        AUTHORS = AUTHORS[21:]
        AUTHORS = AUTHORS[:-3]
        AUTHORS = AUTHORS.rstrip()
        print('Mod authors detected: {}.'.format(AUTHORS))
    except:
        AUTHORS =''

    try:
        URL = getModData('config.cpp','url = ')
        URL = URL[14:]
        URL = URL[:-2]
        URL = URL.rstrip()
        print('Mod url detected: {}.'.format(URL))
    except:
        URL =''

    # check if CBA is used
    CBA = cbaRequired()

    # check if using mod uses stringtables
    try:
        stringTableLable = 'stringtable.xml'
        findStringTable = findFile(stringTableLable, addonsPath)
        if stringTableLable in findStringTable:
            STRINGTABLE = True
    except:
        STRINGTABLE = False

    checkAddonExist(ADDON)
    setUpNewAddon(ADDON,PREFIX,CBA,STRINGTABLE,AUTHOR,AUTHORS,URL)


if __name__ == "__main__":
    sys.exit(main())
