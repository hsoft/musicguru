# Created By: Virgil Dupras
# Created On: 2006/11/18
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os
import os.path as op
from threading import Thread
import tempfile

from AppKit import *
import DiscRecording
import DiscRecordingUI

import hsfs as fs
from hsfs import phys
from hsfs.utils import smart_move
from hsutil import cocoa
from hsutil.conflict import is_conflicted
from hsutil.path import Path
from hsutil.str import format_size

from . import app, sqlfs as sql

(TAG_LOCATIONS,
TAG_DETAILS,
TAG_RECORDED_DISKS) = range(3)

(TAG_DESIGN_BOARD,
TAG_IGNORE_BOX) = range(2)

def WalkDir(base,node_path):
    if not node_path:
        return base
    items = base.dirs + base.files
    return WalkDir(items[node_path[0]],node_path[1:])
    
def ConvertFS(directory):
    if isinstance(directory,fs.manual.Directory):
        root = DiscRecording.DRFolder.alloc().initWithName_(directory.name)
        for child in directory:
            if child.is_container:
                folder = ConvertFS(child)
                root.addChild_(folder)
            else:
                real_child = child.original
                real_path = real_child.path
                if op.exists(unicode(real_path)):
                    file = DiscRecording.DRFile.fileWithPath_(unicode(real_path))
                    file.setBaseName_(child.name)
                    root.addChild_(file)
    else:
        root = DiscRecording.DRFolder.folderWithPath_(unicode(directory.path))
    return root

def GetFirstDevice(must_write_cd=False,must_write_dvd=False):
    devices = DiscRecording.DRDevice.devices()
    for device in devices:
        if (not must_write_cd) or (device.info()['DRDeviceWriteCapabilitiesKey']['DRDeviceCanWriteCDKey']):
            return device

(CT_NONE,
 CT_BLANK,
 CT_NONBLANK) = range(3)

def GetInsertedCDType(device):
    if not device:
        return CT_NONE
    status = device.status()
    if status['DRDeviceMediaStateKey'] == 'DRDeviceMediaStateMediaPresent':
        if status['DRDeviceMediaInfoKey']['DRDeviceMediaIsBlankKey']:
            return CT_BLANK
        else:
            return CT_NONBLANK
    else:
        return CT_NONE

class MusicGuru(app.MusicGuru):
    def __init__(self):
        app.MusicGuru.__init__(self)
        self.progress = cocoa.ThreadedJobPerformer()
        self.song_list = []
        self.info = []
    
    #---Public
    def AddLocation(self, path, name, removeable):
        j = self.progress.create_job()
        def do():
            app.MusicGuru.AddLocation(self, path, name, removeable, j)
        self.progress.run_threaded(do)
    
    def CreateFolderInNode(self, node_path):
        parent = WalkDir(self.board, node_path)
        return app.MusicGuru.new_folder(self, parent)
    
    def GetLocationNames(self,in_board,writable):
        locations = self.board.locations if in_board else self.collection.dirs
        if writable:
            locations = (loc for loc in locations if loc.vol_type != sql.music.VOLTYPE_CDROM)
        return [loc.name for loc in locations]
    
    def GetOutlineBase(self,tag):
        if tag == TAG_IGNORE_BOX:
            return self.board.ignore_box
        else:
            return self.board
    
    def IsNodeConflicted(self,node_path):
        node = WalkDir(self.board,node_path)
        return is_conflicted(node.name)
    
    def IsNodeContainer(self,node_path):
        node = WalkDir(self.board,node_path)
        return node.is_container
    
    def MassRename(self, model, whitespace):
        j = self.progress.create_job()
        def do():
            self.board.MassRename(model, whitespace, j)
        self.progress.run_threaded(do)
    
    def MoveToIgnoreBox(self,node_paths):
        nodes = [WalkDir(self.board,node_path) for node_path in node_paths]
        if nodes:
            smart_move(nodes,self.board.ignore_box,True)
    
    def PerformDrag(self,source_tag,source_node_paths,dest_tag,dest_node_path):
        source_base = self.GetOutlineBase(source_tag)
        dest_base = self.GetOutlineBase(dest_tag)
        sources = (WalkDir(source_base,np) for np in source_node_paths)
        dest = WalkDir(dest_base,dest_node_path)
        sources = [item for item in sources if (item not in dest) and (item is not dest) and (item not in dest.parents)]
        if (not sources) or (not dest.is_container):
            return False
        smart_move(sources,dest,True)
        return True
    
    def RemoveLocationNamed(self,name):
        to_remove = self.collection[name]
        self.board.RemoveLocation(to_remove)
        to_remove.delete()
        
    def RenameNode(self,node_path,new_name):
        #Returns what the node has actually been renamed to
        node = WalkDir(self.board,node_path)
        return super(MusicGuru,self).RenameNode(node,new_name)
    
    def SelectBoardSongs(self,node_paths):
        nodes = (WalkDir(self.board,node_path) for node_path in node_paths)
        originals = [node.original for node in nodes]
        self.info = self.GetSelectionInfo(originals)
    
    def set_location_path(self, location_name, new_path_str):
        location = self.collection[location_name]
        location.initial_path = Path(new_path_str)
    
    def Split(self, model, capacity, grouping_level):
        j = self.progress.create_job()
        def do():
            self.board.Split(model, capacity, grouping_level, 0, j)
        self.progress.run_threaded(do)
    
    def SwitchConflictAndOriginal(self,node_path):
        node = WalkDir(self.board,node_path)
        super(MusicGuru,self).SwitchConflictAndOriginal(node)
    
    def ToggleLocationIndex(self,index):
        location = self.collection.dirs[index]
        self.board.ToggleLocation(location)
    
    def UpdateCollection(self):
        j = self.progress.create_job()
        def do():
            self.collection.update_volumes(j)
        self.progress.run_threaded(do)
    
    def update_location(self, location_name):
        location = self.collection[location_name]
        j = self.progress.create_job()
        def do():
            location.update(None, j)
        self.progress.run_threaded(do)
    
    #---Materialize
    def AddCurrentDisk(self,overwrite):
        dest = self.board.dirs[self.current_burn_index]
        if dest.name in self.collection:
            if not overwrite:
                return False
            self.collection[dest.name].delete()
        #Remove files that don't exist
        for f in dest.allfiles:
            if not op.exists(str(f.original.physical_path)):
                f.delete()
        self.collection.add_volume(dest,dest.name,sql.music.VOLTYPE_CDROM)
        return True
    
    def BurnCurrentDisk(self,window):
        dest = self.board.dirs[self.current_burn_index]
        for location in self.board.locations:
            location.mode = sql.music.MODE_PHYSICAL
        device = GetFirstDevice(True)
        burnfs = ConvertFS(dest)
        track = DiscRecording.DRTrack.trackForRootFolder_(burnfs)
        burn_session = DiscRecording.DRBurn.burnForDevice_(device)
        burn_session.setProperties_({DiscRecording.DRBurnVerifyDiscKey: False});
        panel = DiscRecordingUI.DRBurnProgressPanel.progressPanel().beginProgressSheetForBurn_layout_modalForWindow_(burn_session,track,window)
        for location in self.board.locations:
            location.mode = sql.music.MODE_NORMAL
    
    def CleanBuffer(self):
        dest = self.board.dirs[self.current_burn_index]
        super(MusicGuru,self).CleanBuffer(dest)
    
    def CopyOrMove(self,copy,destination,job,panel):
        def on_need_cd(location):
            return panel.promptForDiskNamed_(location.name)
        
        super(MusicGuru,self).CopyOrMove(copy,destination,job,on_need_cd)
            
    def EjectCDIfNotBlank(self):
        device = GetFirstDevice(True)
        if GetInsertedCDType(device) != CT_BLANK:
            if device:
                Thread(name="ejecting CD",target=device.ejectMedia).start()
            return False
        else:
            return True
    
    def FetchSourceSongs(self,job,panel):
        def on_need_cd(location):
            return panel.promptForDiskNamed_(location.name)
        
        dest = self.board.dirs[self.current_burn_index]
        super(MusicGuru,self).FetchSourceSongs(dest,job,on_need_cd)
    
    def GetBufferSizes(self):
        buffer = self.buffer
        disk_stat = os.statvfs(str(self.collection.buffer_path))
        free_bytes = disk_stat.f_frsize * disk_stat.f_bavail
        minimum = buffer.GetMinimumBytesRequired()
        maximum = buffer.GetMaximumBytesRequired()
        minimum = int(minimum*1.2)
        maximum = max(maximum,minimum)
        buffer.size = int(free_bytes * 0.8)
        return [free_bytes,minimum,maximum,format_size(free_bytes,0,2),format_size(minimum,0,2),format_size(maximum,0,2)]
    
    def PrepareBurning(self):
        self.current_burn_index = 0
        #Getting available disk space on unix:
        #os.statvfs(path) returns the fs stats of path in a structure.
        #The numbers in that struct are in blocks. To get available bytes, we
        #must do s.f_frsize * s.f_bavail (The struct is documented on python.org)
        disk_stat = os.statvfs(tempfile.gettempdir())
        free_bytes = disk_stat.f_frsize * disk_stat.f_bavail
        return super(MusicGuru,self).PrepareBurning(free_bytes)
    
    #---Data
    def GetOutlineViewChildCounts(self, tag, node_path):
        item = WalkDir(self.GetOutlineBase(tag), node_path)
        if item.is_container:
            return [len(subitem) for subitem in item]
        else:
            return []
    
    def GetOutlineViewValues(self,tag,node_path):
        node = WalkDir(self.GetOutlineBase(tag),node_path)
        return self.GetNodeData(node)
    
    def GetTableViewCount(self,tag):
        if tag == TAG_LOCATIONS:
            return len(self.collection.dirs)
        elif tag == TAG_DETAILS:
            return len(self.info)
        elif tag == TAG_RECORDED_DISKS:
            return len(self.board.dirs)
    
    def GetTableViewMarkedIndexes(self,tag):
        if tag == TAG_LOCATIONS:
            return [i for i,directory in enumerate(self.collection.dirs) if directory in self.board.locations]
        return []
    
    def GetTableViewValues(self,tag,row):
        if tag == TAG_LOCATIONS:
            location = self.collection.dirs[row]
            return self.GetLocationData(location)
        elif tag == TAG_DETAILS:
            return self.info[row]
        elif tag == TAG_RECORDED_DISKS:
            cd = self.board.dirs[row]
            return self.GetNodeData(cd)
    
