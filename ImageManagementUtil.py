import os
import shutil
import datetime
import time
from PyQt4.QtCore import QCoreApplication
from PyQt4.Qt import QApplication
import subprocess
import GlobalVar
import logging
import ServerSync

def parseDirectory(Directory):
    head, tail = os.path.split(str(Directory))
    return tail

def parseDirectories(Directories):
    TailNames = []
    for d in Directories:
        QCoreApplication.processEvents()
        d = str(d)
        head, tail = os.path.split(d)
        TailNames.append(tail)
    return TailNames

#loads all the photos within the SourceDirectory but not its subdirectories
def loadAllInDirectory(SourceDirectory):
    if (os.path.isdir(SourceDirectory) == False):
        print SourceDirectory + " is not a valid directory"
        GlobalVar.logger.error(SourceDirectory + " is not a valid directory")

    Paths = [] #list of all the directories to all the images
    filenames= os.listdir(SourceDirectory)
    for filename in filenames:
        if(os.path.isfile(os.path.join(SourceDirectory, filename))):
            continue
        else:
            Paths.append(os.path.join(SourceDirectory, filename))
    return Paths #Array of Image objects

#loads all the photos within the SourceDirectory but also its subdirectories
def loadAllUnderDirectory(SourceDirectory):
    if (os.path.isdir(SourceDirectory) == False):
        print SourceDirectory + " is not a valid directory"
        GlobalVar.logger.error(SourceDirectory + " is not a valid directory")

    ImagePaths = []
    for dirname, dirnames, filenames in os.walk(SourceDirectory):
        for filename in filenames:
            QCoreApplication.processEvents()
            ImagePaths.append( os.path.join(dirname, filename))
    return ImagePaths #Array of Image objects

#Copy and renames a list of photos
def Upload(ImagePaths, DestinationDirectory, PhotographerName,window,Tags):
    Date = datetime.datetime.now().strftime("%Y%m%d")
    ImageNames = []

    #Writing new line into log
    f = open(GlobalVar.UPLOADLOG_LOCATION, "a")
    head, tail = os.path.split(DestinationDirectory)
    f.write(str(datetime.datetime.now().strftime("%m-%d-%Y")) + "," + PhotographerName + "," + tail + "," + str(len(ImagePaths)) + "\n")
    f.close()

    #SyncFile with Server
    t = ServerSync.ThreadClass()
    t.start()

    i=0
    while i<len(ImagePaths): #Renames the images
        Name = str("/" + PhotographerName + "_" + Date + "_") #add the first part of the name on
        for tag in Tags: #adds all the tags
            Name = str(Name + "[" + str(tag) + "]")
        Name = Name + str(parseDirectory(ImagePaths[i]))
        ImageNames.append(Name)
        i+=1

    i=0
    while i<len(ImageNames): #Copy into destination
        QCoreApplication.processEvents()
        try:
            shutil.copy2(ImagePaths[i], str(DestinationDirectory + ImageNames[i]))
        except IOError:
            print "Error: Cannot copy " + ImageNames[i] + " to " + DestinationDirectory
            GlobalVar.logger.error("Error: Cannot copy " + ImageNames[i] + " to " + DestinationDirectory)
        i+=1
        numberuploaded = float(i)
        Progress = numberuploaded/len(ImageNames)*100
        window.pBarUploadProgress.setValue(Progress)
        window.lblCurrentStatus.setText(str(i) + "/" + str(len(ImageNames)) + " uploaded")

    return 0 #0 upon success

#Searches and returns all matches within the Images array
def Search(Paths, Keyword):
    Names = parseDirectories(Paths)
    Results = []
    i=0
    while i<len(Names):
        if str(Keyword).lower() in str(Names[i]).lower():
            Results.append(Paths[i])
        i+=1
    return Results #Array of Image objects

def SearchTags(Paths,Keywords,startDate, endDate):
    Names = parseDirectories(Paths)
    Results = []

    i=0
    while i<len(Names):
        QCoreApplication.processEvents()
        flag  = 0
        if(startDate != 0): #valid dates are entered
            if(startDate.timetuple() <= getImageUploadDate(Names[i]) and endDate.timetuple() >= getImageUploadDate(Names[i])):
                flag=0
            else:
                flag=1
        for keyword in Keywords:
            if str(keyword).lower() not in str(Names[i]).lower():
                flag = 1
        if(flag == 0):
            Results.append(Paths[i])
        i+=1
    return Results #Array of Image objects

#Creates a symbolic link of Images in the DestinationDirectory
def CreateSymLink(ImagePaths, DestinationDirectory):
    os.mkdir(DestinationDirectory)
    for imagepath in ImagePaths:
         try:
             os.symlink(imagepath, str(DestinationDirectory + "/" + parseDirectory(imagepath)))
         except OSError:
             print "Error: Cannot create symbolic link for " + parseDirectory(imagepath) + " to " + DestinationDirectory
             Globalvar.logger.error("Error: Cannot create symbolic link for " + parseDirectory(imagepath) + " to " + DestinationDirectory)
    subprocess.check_call(['open', '--', DestinationDirectory])
    return 0 #0 upon success

def getImageUploadDate(filename):
    parts = filename.split("_")
    if(len(parts[1]) != 8):
        return time.strptime("20000101", "%Y%m%d")
    uploaddate = time.strptime(parts[1], "%Y%m%d")
    return uploaddate

def FileCheck(path, mode):
    try:
        open(path, mode)
    except IOError:
        errorstatement = "Error: file operation on " + path + " failed with mode " + mode
        print errorstatement
        GlobalVar.logger.error(errorstatement)





