# Created By: Virgil Dupras
# Created On: 2006/03/19
# $Id$
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import sys
import objc
from AppKit import *

from hsutil import job

from core import app_cocoa, design

# Fix py2app imports which chokes on relative imports
from core import app, fs_utils, sqlfs
from core.sqlfs import _sql, music, strings, utils
from hsfs import auto, stats, tree, music
from hsfs.phys import music
from hsmedia import aiff, flac, genres, id3v1, id3v2, mp4, mpeg, ogg, wma

class PyMassRenamePanel(NSObject):
    def setRefDir(self,refdir):
        #You MUST call this before starting to use the class
        self.panel = design.MassRenamePanel(refdir)
    
    def changeExampleSong(self):
        self.panel.ChangeExample()
    
    def getExampleDisplayAfter(self):
        return self.panel.example_after
    
    def getExampleDisplayBefore(self):
        return self.panel.example_before
    
    def getModel(self):
        return self.panel.model
    
    def getWhitespace(self):
        return self.panel.whitespace
    
    def setCustomModel_(self,model):
        self.panel.custom_model = model
    
    def setModelSelectedRow_(self,row):
        self.panel.model_index = row
    
    def setWhitespaceSelectedRow_(self,row):
        self.panel.whitespace_index = row
    

class PySplitPanel(NSObject):
    def setRefDir(self,refdir):
        #You MUST call this before starting to use the class
        self.panel = design.SplittingPanel(refdir)
    
    def getGroupingExample(self):
        return self.panel.example
    
    def getCapacity(self):
        return self.panel.capacity
    
    def getGroupingLevel(self):
        return self.panel.grouping_level
    
    def getModel(self):
        return self.panel.model
    
    def setCapacitySelectedRow_(self,row):
        self.panel.capacity_index = row
    
    def setCustomCapacity_(self,capacity):
        self.panel.custom_capacity = capacity
    
    def setCustomModel_(self,model):
        self.panel.custom_model = model
    
    def setGroupingLevel_(self,level):
        self.panel.grouping_level = level
    
    def setModelSelectedRow_(self,row):
        self.panel.model_index = row
    

class PyApp(NSObject):
    pass #fake class

class PyMusicGuru(NSObject):
    def init(self):
        self = super(PyMusicGuru,self).init()
        self.app = app_cocoa.MusicGuru()
        return self
    
    def __CreateJob(self):
        return job.Job(1,lambda p:self.progress.pyUpdate_(p))
    
    #---Locations
    def addLocationWithPath_name_removeable_(self, path, name, removeable):
        return self.app.AddLocation(path, name, removeable)
    
    def canAddLocationWithPath_name_(self,path,name):
        return self.app.CanAddLocation(path,name)
    
    def setPath_ofLocationNamed_(self, path, name):
        self.app.set_location_path(name, path)
    
    def locationNamesInBoard_writable_(self,in_board,writable):
        return self.app.GetLocationNames(in_board,writable)
    
    def removeLocationNamed_(self,name):
        self.app.RemoveLocationNamed(name)
    
    def toggleLocation_(self,index):
        self.app.ToggleLocationIndex(index)
    
    def updateLocationNamed_(self, name):
        self.app.update_location(name)
    
    #---Board
    def conflictCount(self):
        return len(self.app.board.allconflicts)
    
    def emptyBoard(self):
        self.app.board.Empty()
    
    def getBoardStats(self):
        return self.app.board.stats_line
    
    def getMassRenamePanel(self):
        result = PyMassRenamePanel.alloc().init()
        result.setRefDir(self.app.board)
        return result
    
    def getSplitPanel(self):
        result = PySplitPanel.alloc().init()
        result.setRefDir(self.app.board)
        return result
    
    def isNodeConflicted_(self,node_path):
        return self.app.IsNodeConflicted(node_path)
    
    def isBoardSplitted(self):
        return self.app.board.splitted
    
    def massRenameWithModel_whitespaceType_(self, model, whitespace):
        self.app.MassRename(model, whitespace)
    
    def moveConflicts(self):
        #Returns true is at least one conflict has been moved
        return self.app.board.MoveConflicts()
    
    def moveConflictsAndOriginals(self):
        #Returns true is at least one conflict has been moved
        return self.app.board.MoveConflicts(True)
    
    def moveToIgnoreBox_(self,node_paths):
        self.app.MoveToIgnoreBox(node_paths)
    
    def newFolderIn_(self,node_path):
        return self.app.CreateFolderInNode(node_path)
    
    def performDragFrom_withNodes_to_withNode_(self,source_tag,source_node_paths,dest_tag,dest_node_path):
        return self.app.PerformDrag(source_tag,source_node_paths,dest_tag,dest_node_path)
    
    def removeEmptyFolders(self):
        self.app.RemoveEmptyDirs()
    
    def renameNode_to_(self,node_path,new_name):
        return self.app.RenameNode(node_path,new_name)
    
    def selectBoardSongs_(self,node_paths):
        self.app.SelectBoardSongs(node_paths)
    
    def splitWithModel_capacity_groupingLevel_(self, model, capacity, grouping_level):
        if self.app.board.splitted:
            return
        self.app.Split(model, capacity, grouping_level)
    
    def switchConflictAndOriginal_(self,node_path):
        self.app.SwitchConflictAndOriginal(node_path)
    
    def unsplit(self):
        self.app.board.Unsplit()
    
    #---Materialize
    def addCurrentDiskToMPLOverwrite_(self,overwrite):
        return self.app.AddCurrentDisk(overwrite)
    
    def burnCurrentDiskWithWindow_(self,window):
        self.app.BurnCurrentDisk(window)
    
    def cleanBuffer(self):
        self.app.CleanBuffer()
    
    def copyOrMove_toPath_onNeedCDPanel_(self,copy,destination,panel):
        self.app.CopyOrMove(copy,destination,self.__CreateJob(),panel)
    
    def ejectCDIfNotBlank(self):
        return self.app.EjectCDIfNotBlank()
    
    def fetchSourceSongsWithNeedCDPanel_(self,panel):
        self.app.FetchSourceSongs(self.__CreateJob(),panel)
    
    def getBurnBufferSizes(self):
        return self.app.GetBufferSizes()
    
    def getDestinationDiskName(self):
        return self.app.board.dirs[self.app.current_burn_index].name
    
    def isFinishedBurning(self):
        return self.app.current_burn_index >= len(self.app.board.dirs)
    
    def prepareBurning(self):
        return self.app.PrepareBurning()
    
    def prepareNextCDToBurn(self):
        self.app.current_burn_index += 1
    
    def renameInRespectiveLocations(self):
        self.app.RenameInRespectiveLocations(self.__CreateJob())
    
    #---Misc
    def isNodeContainer_(self,node_path):
        return self.app.IsNodeContainer(node_path)
    
    def updateCollection(self):
        self.app.UpdateCollection()
    
    #---Data
    @objc.signature('i@:i')
    def getOutlineViewMaxLevel_(self, tag):
        return 0 # no max level
    
    @objc.signature('@@:i@')
    def getOutlineView_childCountsForPath_(self, tag, node_path):
        return self.app.GetOutlineViewChildCounts(tag, node_path)
    
    def getOutlineView_valuesForIndexes_(self,tag,node_path):
        return self.app.GetOutlineViewValues(tag,node_path)
    
    def getOutlineView_markedAtIndexes_(self,tag,node_path):
        return False
    
    def getTableViewCount_(self,tag):
        return self.app.GetTableViewCount(tag)
    
    def getTableViewMarkedIndexes_(self,tag):
        return self.app.GetTableViewMarkedIndexes(tag)
    
    def getTableView_valuesForRow_(self,tag,row):
        return self.app.GetTableViewValues(tag,row)
    
    #---Worker
    def getJobProgress(self):
        return self.app.progress.last_progress
    
    def getJobDesc(self):
        return self.app.progress.last_desc
    
    def cancelJob(self):
        self.app.progress.job_cancelled = True
    
    #---Registration
    @objc.signature('i@:')
    def isRegistered(self):
        return self.app.registered
    
    @objc.signature('i@:@@')
    def isCodeValid_withEmail_(self, code, email):
        return self.app.is_code_valid(code, email)
    
    def setRegisteredCode_andEmail_(self, code, email):
        self.app.set_registration(code, email)
    

