import os
import GlobalVar
import logging
import ImageManagementUtil

def getEventDirectory():
    ImageManagementUtil.FileCheck(GlobalVar.CONFIGFILE_LOCATION, "r+")
    f = open(GlobalVar.CONFIGFILE_LOCATION, "r+") #Open for reading and writing because in case file does not exist
    lines = f.readlines()
    f.close()
    for line in lines:
        if "#EventDirectory# " in line:
            line = line.replace("#EventDirectory# ", "")
            return line  #return a string of the directory
    return "" #return nothing if not found

def getSourceDirectory():
    ImageManagementUtil.FileCheck(GlobalVar.CONFIGFILE_LOCATION, "r+")
    f = open(GlobalVar.CONFIGFILE_LOCATION, "r+") #Open for reading and writing because in case file does not exist
    lines = f.readlines()
    f.close()
    for line in lines:
        if "#SourceDirectory# " in line:
            line = line.replace("#SourceDirectory# ", "")
            return line  #return a string of the directory
    return "" #return nothing if not found

def getSymLinkDirectory():
    ImageManagementUtil.FileCheck(GlobalVar.CONFIGFILE_LOCATION, "r+")
    f = open(GlobalVar.CONFIGFILE_LOCATION, "r+") #Open for reading and writing because in case file does not exist
    lines = f.readlines()
    f.close()
    for line in lines:
        if "#SymLinkDirectory# " in line:
            line = line.replace("#SymLinkDirectory# ", "")
            return line  #return a string of the directory
    return "" #return nothing if not found

def getDestinationDirectory():
    ImageManagementUtil.FileCheck(GlobalVar.CONFIGFILE_LOCATION, "r+")
    f = open(GlobalVar.CONFIGFILE_LOCATION, "r+") #Open for reading and writing because in case file does not exist
    lines = f.readlines()
    f.close()
    for line in lines:
        if "#DestinationDirectory# " in line:
            line = line.replace("#DestinationDirectory# ", "")
            return line  #return a string of the directory
    return "" #return nothing if not found

def setDestinationDirectory(NewDirectory):
    if(os.path.isfile(GlobalVar.CONFIGFILE_LOCATION) == False):
        f = open(GlobalVar.CONFIGFILE_LOCATION, "w") #Open for reading and writing because in case file does not exist
        f.close()
    #Reads all the files in
    f = open(GlobalVar.CONFIGFILE_LOCATION, "r+") #Open for reading and writing because in case file does not exist
    lines = f.readlines()
    f.close()

    f = open(GlobalVar.CONFIGFILE_LOCATION, "w")
    written = False
    for line in lines:
        if "#DestinationDirectory# " in line:
            f.write("#DestinationDirectory# " + NewDirectory + "\n")
            written = True
        else:
            f.write(line)
    f.close()

    if written == False:
        f = open(GlobalVar.CONFIGFILE_LOCATION, "a")
        f.write("#DestinationDirectory# " + NewDirectory + "\n")
        f.close()
        return 1 #if #DestinationDiretory did not exist
    return 0 #if everything executed as expected

def setSourceDirectory(NewDirectory):
    if(os.path.isfile(GlobalVar.CONFIGFILE_LOCATION) == False):
        f = open(GlobalVar.CONFIGFILE_LOCATION, "w") #Open for reading and writing because in case file does not exist
        f.close()

    #Reads all the files in
    f = open(GlobalVar.CONFIGFILE_LOCATION, "r+") #Open for reading and writing because in case file does not exist
    lines = f.readlines()
    f.close()

    f = open(GlobalVar.CONFIGFILE_LOCATION, "w")
    written = False
    for line in lines:
        if "#SourceDirectory# " in line:
            f.write("#SourceDirectory# " + NewDirectory + "\n")
            written = True
        else:
            f.write(line)
    f.close()

    if written == False:
        f = open(GlobalVar.CONFIGFILE_LOCATION, "a")
        f.write("#SourceDirectory# " + NewDirectory + "\n")
        f.close()
        return 1 #if #DestinationDiretory did not exist
    return 0 #if everything executed as expected

def setSymLinkDirectory(NewDirectory):
    if(os.path.isfile(GlobalVar.CONFIGFILE_LOCATION) == False):
        f = open(GlobalVar.CONFIGFILE_LOCATION, "w") #Open for reading and writing because in case file does not exist
        f.close()
    #Reads all the files in
    f = open(GlobalVar.CONFIGFILE_LOCATION, "r+") #Open for reading and writing because in case file does not exist
    lines = f.readlines()
    f.close()

    f = open(GlobalVar.CONFIGFILE_LOCATION, "w")
    written = False
    for line in lines:
        if "#SymLinkDirectory# " in line:
            f.write("#SymLinkDirectory# " + NewDirectory + "\n")
            written = True
        else:
            f.write(line)
    f.close()

    if written == False:
        f = open(GlobalVar.CONFIGFILE_LOCATION, "a")
        f.write("#SymLinkDirectory# " + NewDirectory + "\n")
        f.close()
        return 1 #if #DestinationDiretory did not exist
    return 0 #if everything executed as expected