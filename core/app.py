# Created By: Virgil Dupras
# Created On: 2006/11/18
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os
import os.path as op
import shutil

import hsfs as fs
from hsfs import phys
from hsfs.stats import StatsList
from hsutil.conflict import get_unconflicted_name, get_conflicted_name
from hsutil.files import clean_empty_dirs
from hsutil.misc import cond, tryint
from hsutil.str import format_size, format_time, multi_replace, FT_MINUTES, FS_FORBIDDEN
from hscommon.job import JobCancelled
from hscommon.reg import RegistrableApplication

from . import design
from .fs_utils import BatchOperation
from .sqlfs.music import Root, VOLTYPE_CDROM, VOLTYPE_FIXED, MODE_PHYSICAL, MODE_NORMAL

class MusicGuru(RegistrableApplication):
    VERSION = '1.4.1'
    DEMO_LIMIT_DESC = "In the demo version, it's not possible to materialize designs."
    
    def __init__(self, appdata=None):
        RegistrableApplication.__init__(self, appid=2)
        if appdata is None:
            appdata = op.expanduser(op.join('~', '.hsoftdata', 'musicguru'))
        self.appdata = appdata
        if not op.exists(self.appdata):
            os.makedirs(self.appdata)
        self.collection = Root(op.join(appdata, 'music.db'))
        self.board = design.Board()
    
    def AddLocation(self, path, name, removeable, job):
        vol_type = cond(removeable, VOLTYPE_CDROM, VOLTYPE_FIXED)
        ref = phys.music.Directory(None, path)
        self.collection.add_volume(ref, name, vol_type, job)
    
    def CanAddLocation(self, path, name):
        #returns None is it is possible to add the location, and returns the error msg otherwise.
        if not name:
            return "A location cannot have an empty name."
        if name in self.collection:
            return "'%s' is already in your collection. Choose another name." % name
        if (not path) or (not os.path.exists(path)):
            return "'%s' is not a valid directory." % path
        already_there = [location for location in self.collection 
            if (location.vol_type != VOLTYPE_CDROM) and (str(location.physical_path) == path)]
        if already_there:
            return "The directory '%s' is already in your collection as the location '%s'." % (path,already_there[0].name)
        return ""
    
    def GetSelectionInfo(self, item):
        def output_stats(info, item):
            info.append(('Size',format_size(item.get_stat('size'),2)))
            info.append(('Time',format_time(item.get_stat('duration'),FT_MINUTES)))
            info.append(('Extensions',','.join(item.get_stat('extension',[]))))
            info.append(('# Artists',len(item.get_stat('artist',[]))))
            info.append(('# Albums',len(item.get_stat('album',[]))))
            info.append(('# Genres',len(item.get_stat('genre',[]))))
            stats = item.get_stat('year',[])
            years = [tryint(s) for s in stats if s]
            if not years:
                years = [0]
            minyear = min(years)
            maxyear = max(years)
            info.append(('Years',"%d - %d" % (minyear,maxyear)))
        
        new_info = []
        if isinstance(item,list) and (len(item) == 1):
            item = item[0]
        if isinstance(item,list):
            if item:
                new_item = StatsList()
                #remove all items with their parent in the list
                new_item += [child for child in item if child.parent not in item]
                new_info.append(('Selection',"%d selected" % len(item)))
                filecount = new_item.get_stat('filecount')
                if filecount is None:
                    filecount = 0
                filecount += len([child for child in new_item if not child.is_container])
                new_info.append(('Songs',filecount))
                output_stats(new_info,new_item)
        elif item.is_container:
            new_info.append(('Path',unicode(item.path[1:])))
            new_info.append(('Songs',item.get_stat('filecount')))
            output_stats(new_info,item)
        else:
            new_info.append(('Filename',item.name))
            new_info.append(('Directory',unicode(item.parent.path[1:])))
            new_info.append(('Title',item.title))
            new_info.append(('Artist',item.artist))
            new_info.append(('Album',item.album))
            new_info.append(('Genre',item.genre))
            new_info.append(('Year',item.year))
            new_info.append(('Track',"%02d" % item.track))
            new_info.append(('Size',format_size(item.size,2)))
            new_info.append(('Time',format_time(item.duration,FT_MINUTES)))
            new_info.append(('Bitrate',item.bitrate))
            new_info.append(('Comment',item.comment))
        return new_info
    
    def new_folder(self, parent):
        new_name = get_conflicted_name(parent, 'New Folder')
        new_folder = fs.manual.AutoMerge(parent, new_name)
        return new_folder.name
    
    def RemoveEmptyDirs(self):
        self.board.clean_empty_dirs()
        self.board.ignore_box.clean_empty_dirs()
        
    def RenameNode(self,node,new_name):
        #Returns what the node has actually been renamed to
        node.name = multi_replace(new_name,FS_FORBIDDEN)
        return node.name
    
    def SwitchConflictAndOriginal(self,node):
        original_name = get_unconflicted_name(node.name)
        try:
            original = node.parent[original_name]
            old_name = node.name
            original.name = '__switching__'
            node.name = original_name
            original.name = old_name
        except KeyError:
            node.name = original_name
        return original
    
    #---Materialize
    def CopyOrMove(self,copy,destination,job,on_need_cd):
        job = job.start_subjob(2)
        for location in self.board.locations:
            location.mode = MODE_PHYSICAL
        try:
            bo = BatchOperation(self.board,destination)
            bo.OnNeedCD = on_need_cd
            if copy:
                bo.copy(job)
            else:
                bo.rename(job)
            for location in self.board.locations:
                if location.vol_type != VOLTYPE_CDROM:
                    try:
                        clean_empty_dirs(location.path, files_to_delete=['.DS_Store'])
                    except EnvironmentError:
                        pass
                location.mode = MODE_NORMAL
            self.collection.update_volumes(job)
        except JobCancelled:
            for location in self.board.locations:
                location.mode = MODE_NORMAL
    
    def RenameInRespectiveLocations(self,job):
        #XXX Refactor: Return value isn't used in any gui port.
        for location in self.board.locations:
            if location.vol_type == VOLTYPE_CDROM:
                return 1
        j = job.start_subjob(len(self.board.locations) + 1)
        try:
            for location in self.board.locations:
                location.mode = MODE_PHYSICAL
                destination = location.path
                source_list = [song for song in self.board.allfiles if location in song.original.parents]
                bo = BatchOperation(source_list,destination)
                bo.rename(j)
                try:
                    clean_empty_dirs(location.path, files_to_delete=['.DS_Store'])
                except EnvironmentError:
                    pass
                location.mode = MODE_NORMAL
            self.collection.update_volumes(j)
            return 0
        except JobCancelled:
            return 2
