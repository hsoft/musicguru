# Created By: Virgil Dupras
# Created On: 2006/11/18
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.conflict import is_conflicted
from hscommon.util import dedupe, format_size, format_time
from hscommon.path import Path
from hscommon import cocoa

from . import app, sqlfs as sql
from .fs_utils import smart_move

(TAG_LOCATIONS,
TAG_DETAILS,
TAG_RECORDED_DISKS) = list(range(3))

(TAG_DESIGN_BOARD,
TAG_IGNORE_BOX) = list(range(2))

def WalkDir(base,node_path):
    if not node_path:
        return base
    items = base.dirs + base.files
    return WalkDir(items[node_path[0]],node_path[1:])
    
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
    def CopyOrMove(self, copy, destination, panel):
        def on_need_cd(location):
            return panel.promptForDiskNamed_(location.name)
        
        j = self.progress.create_job()
        def do():
            super(MusicGuru, self).CopyOrMove(copy, destination, j, on_need_cd)
        self.progress.run_threaded(do)
    
    def RenameInRespectiveLocations(self):
        j = self.progress.create_job()
        def do():
            super(MusicGuru, self).RenameInRespectiveLocations(j)
        self.progress.run_threaded(do)
    
    #---Data
    def GetNodeData(self, node):
        if node.is_container:
            img_name = 'folder_conflict_16' if node.allconflicts else 'folder_16'
            parent_volumes = dedupe(song.original.parent_volume for song in node.iterallfiles())
            return [
                node.name,
                ','.join(l.name for l in parent_volumes),
                node.get_stat('filecount'),
                format_size(node.get_stat('size'),2,2,False),
                format_time(node.get_stat('duration')),
                img_name,
            ]
        else:
            img_name = 'song_conflict_16' if is_conflicted(node.name) else 'song_16'
            return [
                node.name,
                node.original.parent_volume.name,
                0,
                format_size(node.size,2,2,False),
                format_time(node.duration, with_hours=False),
                img_name,
            ]
    
    def GetLocationData(self, location):
        return [
            location.name,
            location.get_stat('filecount'),
            format_size(location.get_stat('size'),2,3,False),
            location.is_removable,
            location.is_available,
            str(location.physical_path)
        ]
    
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
    
