# Created By: Virgil Dupras
# Created On: 2006/03/19
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys
import objc

from hscommon import job
from hscommon.cocoa.inter import signature, PyFairware
from hscommon.cocoa.objcmin import NSObject

from core import app_cocoa, design

# Fix py2app imports which chokes on relative imports
from core import app, fs_utils, sqlfs
from core.sqlfs import _sql, music, strings, utils
from hsfs import auto, stats, tree, music
from hsfs.phys import music
from hsaudiotag import aiff, flac, genres, id3v1, id3v2, mp4, mpeg, ogg, wma

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

class PyMusicGuru(PyFairware):
    def init(self):
        self = super(PyMusicGuru,self).init()
        self.py = app_cocoa.MusicGuru()
        return self
    
    #---Locations
    def addLocationWithPath_name_removeable_(self, path, name, removeable):
        return self.py.AddLocation(path, name, removeable)
    
    def canAddLocationWithPath_name_(self,path,name):
        return self.py.CanAddLocation(path,name)
    
    def setPath_ofLocationNamed_(self, path, name):
        self.py.set_location_path(name, path)
    
    def locationNamesInBoard_writable_(self,in_board,writable):
        return self.py.GetLocationNames(in_board,writable)
    
    def removeLocationNamed_(self,name):
        self.py.RemoveLocationNamed(name)
    
    def toggleLocation_(self,index):
        self.py.ToggleLocationIndex(index)
    
    def updateLocationNamed_(self, name):
        self.py.update_location(name)
    
    #---Board
    def conflictCount(self):
        return len(self.py.board.allconflicts)
    
    def emptyBoard(self):
        self.py.board.Empty()
    
    def getBoardStats(self):
        return self.py.board.stats_line
    
    def getMassRenamePanel(self):
        result = PyMassRenamePanel.alloc().init()
        result.setRefDir(self.py.board)
        return result
    
    def getSplitPanel(self):
        result = PySplitPanel.alloc().init()
        result.setRefDir(self.py.board)
        return result
    
    def isNodeConflicted_(self,node_path):
        return self.py.IsNodeConflicted(node_path)
    
    def isBoardSplitted(self):
        return self.py.board.splitted
    
    def massRenameWithModel_whitespaceType_(self, model, whitespace):
        self.py.MassRename(model, whitespace)
    
    def moveConflicts(self):
        #Returns true is at least one conflict has been moved
        return self.py.board.MoveConflicts()
    
    def moveConflictsAndOriginals(self):
        #Returns true is at least one conflict has been moved
        return self.py.board.MoveConflicts(True)
    
    def moveToIgnoreBox_(self,node_paths):
        self.py.MoveToIgnoreBox(node_paths)
    
    def newFolderIn_(self,node_path):
        return self.py.CreateFolderInNode(node_path)
    
    def performDragFrom_withNodes_to_withNode_(self,source_tag,source_node_paths,dest_tag,dest_node_path):
        return self.py.PerformDrag(source_tag,source_node_paths,dest_tag,dest_node_path)
    
    def removeEmptyFolders(self):
        self.py.RemoveEmptyDirs()
    
    def renameNode_to_(self,node_path,new_name):
        return self.py.RenameNode(node_path,new_name)
    
    def selectBoardSongs_(self,node_paths):
        self.py.SelectBoardSongs(node_paths)
    
    def splitWithModel_capacity_groupingLevel_(self, model, capacity, grouping_level):
        if self.py.board.splitted:
            return
        self.py.Split(model, capacity, grouping_level)
    
    def switchConflictAndOriginal_(self,node_path):
        self.py.SwitchConflictAndOriginal(node_path)
    
    def unsplit(self):
        self.py.board.Unsplit()
    
    #---Materialize
    def copyOrMove_toPath_onNeedCDPanel_(self,copy,destination,panel):
        self.py.CopyOrMove(copy, destination, panel)
    
    def renameInRespectiveLocations(self):
        self.py.RenameInRespectiveLocations()
    
    #---Misc
    def isNodeContainer_(self,node_path):
        return self.py.IsNodeContainer(node_path)
    
    def updateCollection(self):
        self.py.UpdateCollection()
    
    #---Data
    @signature('i@:i')
    def getOutlineViewMaxLevel_(self, tag):
        return 0 # no max level
    
    @signature('@@:i@')
    def getOutlineView_childCountsForPath_(self, tag, node_path):
        return self.py.GetOutlineViewChildCounts(tag, node_path)
    
    def getOutlineView_valuesForIndexes_(self,tag,node_path):
        return self.py.GetOutlineViewValues(tag,node_path)
    
    def getOutlineView_markedAtIndexes_(self,tag,node_path):
        return False
    
    def getTableViewCount_(self,tag):
        return self.py.GetTableViewCount(tag)
    
    def getTableViewMarkedIndexes_(self,tag):
        return self.py.GetTableViewMarkedIndexes(tag)
    
    def getTableView_valuesForRow_(self,tag,row):
        return self.py.GetTableViewValues(tag,row)
    
    #---Worker
    def getJobProgress(self):
        return self.py.progress.last_progress
    
    def getJobDesc(self):
        return self.py.progress.last_desc
    
    def cancelJob(self):
        self.py.progress.job_cancelled = True
    
    def jobCompleted_(self, jobid):
        pass
    
    #---Registration
    def appName(self):
        return "musicGuru"
    

