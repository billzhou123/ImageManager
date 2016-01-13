from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature
import ImageManagementUtil
import GlobalVar
import ConfigIO
import datetime
import time
import os
from Ui_MainIU import *
from PyQt4 import QtCore, QtGui
import subprocess

class MainWindow(QMainWindow, Ui_MainWindow):

    #Initiate the window
    def __init__(self, parent = None):
        GlobalVar.SourceDirectory = str(ConfigIO.getSourceDirectory()).replace('\n', '').replace('\t', '').replace('\r', '')
        GlobalVar.DestinationDirectory = ""
        GlobalVar.EventDirectory = str(ConfigIO.getEventDirectory()).replace('\n', '').replace('\t', '').replace('\r', '')
        GlobalVar.SymLinkDirectory = str(ConfigIO.getSymLinkDirectory()).replace('\n', '').replace('\t', '').replace('\r', '')
        GlobalVar.AllPhotoPaths = ImageManagementUtil.loadAllUnderDirectory(GlobalVar.EventDirectory)
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        GlobalVar.EventPaths = ImageManagementUtil.loadAllInDirectory(GlobalVar.EventDirectory)
        GlobalVar.EventNames = ImageManagementUtil.parseDirectories(GlobalVar.EventPaths)
        self.lWidgetEvent.addItems(GlobalVar.EventNames)
        self.lcdNumberTotalImages.display(len(GlobalVar.AllPhotoPaths))
        self.btnUpload.setEnabled(False)

    #When user selects an event
    def on_lWidgetEvent_itemClicked(self):
        print "Event Active"
        GlobalVar.EventSelected = True
        if(GlobalVar.EventSelected == True and GlobalVar.PhotographerNameEntered == True and GlobalVar.PhotoSelected == True):
            self.btnUpload.setEnabled(True)

    #When user selects a photographer
    def on_cBoxPhotographer_currentIndexChanged(self):
        if(self.cBoxPhotographer.currentIndex() != 0):
            GlobalVar.PhotographerNameEntered = True
        else:
            GlobalVar.PhotographerNameEntered = False

        if(GlobalVar.EventSelected == True and GlobalVar.PhotographerNameEntered == True and GlobalVar.PhotoSelected == True):
            self.btnUpload.setEnabled(True)

    #When user selects photos to upload
    def on_btnBrowse_released(self):
        self.lWidgetPhotoPath.clear()
        l = QListWidget()
        GlobalVar.ImagePaths = QtGui.QFileDialog.getOpenFileNames(QFileDialog(), 'Open file', GlobalVar.SourceDirectory)
        self.lWidgetPhotoPath.addItems(ImageManagementUtil.parseDirectories(GlobalVar.ImagePaths))
        self.lblNumberSelected.setText(str(len(GlobalVar.ImagePaths)) + " Selected")
        GlobalVar.PhotoSelected = True
        if(GlobalVar.EventSelected == True and GlobalVar.PhotographerNameEntered == True and GlobalVar.PhotoSelected == True):
            self.btnUpload.setEnabled(True)

    #When user clears the list of photos to be uploaded
    def on_btnClear_clicked(self):
        GlobalVar.ImagePaths = []
        self.lWidgetPhotoPath.clear()
        GlobalVar.PhotoSelected == False
        self.btnUpload.setEnabled(False)
        self.pBarUploadProgress.setValue(0)
        self.lblCurrentStatus.setText("Idle")

    #When user requests the refresh the events list
    def on_btnRefreshEvents_released(self):
        self.lWidgetEvent.clear()
        GlobalVar.EventPaths = ImageManagementUtil.loadAllInDirectory(GlobalVar.EventDirectory)
        GlobalVar.EventNames = ImageManagementUtil.parseDirectories(GlobalVar.EventPaths)
        self.lWidgetEvent.addItems(GlobalVar.EventNames)

    #When user starts typing in the EventSelector search box
    def on_lEditEventPicker_textChanged(self):
        keyword = self.lEditEventPicker.text()
        ResultEventPaths = ImageManagementUtil.Search(GlobalVar.EventPaths,keyword)
        self.lWidgetEvent.clear()
        self.lWidgetEvent.addItems(ImageManagementUtil.parseDirectories(ResultEventPaths))

    #When user hits 'Enter' in the EventSelector search box
    def on_lEditEventPicker_returnPressed(self):
        keyword = self.lEditEventPicker.text()
        ResultEventPaths = ImageManagementUtil.Search(GlobalVar.EventPaths,keyword)
        self.lWidgetEvent.clear()
        self.lWidgetEvent.addItems(ImageManagementUtil.parseDirectories(ResultEventPaths))

    #When user clicks the 'Upload' button
    def on_btnUpload_released(self):
        GlobalVar.Tags.append(str(self.lWidgetEvent.currentItem().text()))
        if(self.cBoxSenior.checkState() == 2):
            GlobalVar.Tags.append("Senior")
        if(self.cBoxJunior.checkState() == 2):
            GlobalVar.Tags.append("Junior")
        if(self.cBoxSophomore.checkState() == 2):
            GlobalVar.Tags.append("Sophomore")
        if(self.cBoxFreshmen.checkState() == 2):
            GlobalVar.Tags.append("Freshmen")
        if(self.lEditOpponent.text() != ""):
            GlobalVar.Tags.append("vs" + str(self.lEditOpponent.text()).replace(" ",""))
        if(self.cBoxStudentLife.checkState() == 2):
            GlobalVar.Tags.append("StudentLife")
        if(self.cBoxAcademics.checkState() == 2):
            GlobalVar.Tags.append("Academics")
        if(self.cBoxSports.checkState() == 2):
            GlobalVar.Tags.append("Sports")
        if(self.cBoxPeople.checkState() == 2):
            GlobalVar.Tags.append("People")
        if(self.cBoxClubs.checkState() == 2):
            GlobalVar.Tags.append("Clubs")
        if(self.cBoxCrowds.checkState() == 2):
            GlobalVar.Tags.append("Crowds")

        Photographer = self.cBoxPhotographer.currentText()
        DestinationDirectory = GlobalVar.EventDirectory + "/" + str(self.lWidgetEvent.currentItem().text())
        ImageManagementUtil.Upload(GlobalVar.ImagePaths,DestinationDirectory,Photographer,self, GlobalVar.Tags)

    def on_btnShowInFolder_released(self):
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        dir = GlobalVar.SymLinkDirectory + "/" + "Linked" + str(now)
        print dir
        ImageManagementUtil.CreateSymLink(GlobalVar.TagSearchResultPaths,dir)

    def on_btnClearTagSearch_released(self):
        self.lWidgetTagSearchResults.clear()
        GlobalVar.TagSearchResultPaths = []

    def on_lWidgetTagSearchResults_itemDoubleClicked(self):
        if(GlobalVar.EventDoubleClicked == True):
            GlobalVar.EventDoubleClicked = False
            return

        index = self.lWidgetTagSearchResults.currentRow()
        print index
        subprocess.call(['open', GlobalVar.TagSearchResultPaths[index]])

    def on_lEditTagSearch_textChanged(self):
        startdate = self.dEditStart.date().toPyDate()
        enddate = self.dEditEnd.date().toPyDate()
        if(len(str(self.lEditTagSearch.text()))> 3): #only performs type and search if search terms are longer than 3 characters
            if((enddate - startdate).days > 0 and (enddate - startdate).days < GlobalVar.DATESEARCHTOLERANCE): #If the time interval qualifies the conditions
                Keywords = str(self.lEditTagSearch.text()).split()
                GlobalVar.TagSearchResultPaths = ImageManagementUtil.SearchTags(GlobalVar.AllPhotoPaths,Keywords, startdate,enddate)
                self.lWidgetTagSearchResults.clear()
                self.lWidgetTagSearchResults.addItems(ImageManagementUtil.parseDirectories(GlobalVar.TagSearchResultPaths))
            else: #if it does not meet conditions
                Keywords = str(self.lEditTagSearch.text()).split()
                GlobalVar.TagSearchResultPaths = ImageManagementUtil.SearchTags(GlobalVar.AllPhotoPaths,Keywords,0,0)
                self.lWidgetTagSearchResults.clear()
                self.lWidgetTagSearchResults.addItems(ImageManagementUtil.parseDirectories(GlobalVar.TagSearchResultPaths))
        else:
            if((enddate - startdate).days < 0 or (enddate - startdate).days > GlobalVar.DATESEARCHTOLERANCE): #only clear if does not meet date conditions
                self.lWidgetTagSearchResults.clear()
                GlobalVar.TagSearchResultPaths = []

    def on_dEditStart_dateChanged(self):
        startdate = self.dEditStart.date().toPyDate()
        enddate = self.dEditEnd.date().toPyDate()

        if((enddate - startdate).days > 0 and (enddate - startdate).days < GlobalVar.DATESEARCHTOLERANCE): #If the time interval qualifies the conditions
            Keywords = str(self.lEditTagSearch.text()).split()
            GlobalVar.TagSearchResultPaths = ImageManagementUtil.SearchTags(GlobalVar.AllPhotoPaths,Keywords,startdate,enddate)
            self.lWidgetTagSearchResults.clear()
            self.lWidgetTagSearchResults.addItems(ImageManagementUtil.parseDirectories(GlobalVar.TagSearchResultPaths))
        else:
            self.lWidgetTagSearchResults.clear()
            GlobalVar.TagSearchResultPaths = []

    def on_dEditEnd_dateChanged(self):
        startdate = self.dEditStart.date().toPyDate()
        enddate = self.dEditEnd.date().toPyDate()

        if((enddate - startdate).days > 0 and (enddate - startdate).days < GlobalVar.DATESEARCHTOLERANCE): #If the time interval qualifies the conditions
            Keywords = str(self.lEditTagSearch.text()).split()
            GlobalVar.TagSearchResultPaths = ImageManagementUtil.SearchTags(GlobalVar.AllPhotoPaths,Keywords,startdate,enddate)
            self.lWidgetTagSearchResults.clear()
            self.lWidgetTagSearchResults.addItems(ImageManagementUtil.parseDirectories(GlobalVar.TagSearchResultPaths))
        else:
            self.lWidgetTagSearchResults.clear()
            GlobalVar.TagSearchResultPaths = []

    def on_btnResetDateFilter_released(self):
        self.dEditStart.setDate(QtCore.QDate(2014, 6, 1))
        self.dEditEnd.setDate(QtCore.QDate(2015, 4, 1))
        if(len(str(self.lEditTagSearch.text()))> 3):
            Keywords = str(self.lEditTagSearch.text()).split()
            GlobalVar.TagSearchResultPaths = ImageManagementUtil.SearchTags(GlobalVar.AllPhotoPaths,Keywords,0,0)
            self.lWidgetTagSearchResults.clear()
            self.lWidgetTagSearchResults.addItems(ImageManagementUtil.parseDirectories(GlobalVar.TagSearchResultPaths))
        else:
            self.lWidgetTagSearchResults.clear()
            GlobalVar.TagSearchResultPaths = []

    def on_btnTagSearchRefresh_released(self):
        GlobalVar.AllPhotoPaths = ImageManagementUtil.loadAllUnderDirectory(GlobalVar.EventDirectory)
        self.lcdNumberTotalImages.display(len(GlobalVar.AllPhotoPaths))

    def on_lEditSearchOpponent_returnPressed(self):
        text = str(self.lEditTagSearch.text()) + str(self.lEditSearchOpponent.text())
        self.lEditTagSearch.setText(text)
        self.lEditSearchOpponent.clear()

    def on_cBoxSearchSenior_stateChanged(self):
        if(self.cBoxSearchSenior.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " senior"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchJunior_stateChanged(self):
        if(self.cBoxSearchJunior.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " junior"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchSophomore_stateChanged(self):
        if(self.cBoxSearchSophomore.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " sophomore"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchFreshmen_stateChanged(self):
        if(self.cBoxSearchFreshmen.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " freshmen"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchPeople_stateChanged(self):
        if(self.cBoxSearchPeople.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " people"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchAcademics_stateChanged(self):
        if(self.cBoxSearchAcademics.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " academics"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchStudentLife_stateChanged(self):
        if(self.cBoxSearchStudentLife.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " StudentLife"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchClubs_stateChanged(self):
        if(self.cBoxSearchClubs.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " clubs"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchSports_stateChanged(self):
        if(self.cBoxSearchSports.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " Sports"
            self.lEditTagSearch.setText(text)
    def on_cBoxSearchCrowds_stateChanged(self):
        if(self.cBoxSearchCrowds.checkState() == 2): #adds the tag to the text
            text = str(self.lEditTagSearch.text()) + " Crowds"
            self.lEditTagSearch.setText(text)






























