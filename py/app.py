#!/usr/bin/env python
"""
Unit Name: musicguru.app
Created By: Virgil Dupras
Created On: 2006/11/18
Last modified by:$Author: virgil $
Last modified on:$Date: 2009-02-28 17:16:32 +0100 (Sat, 28 Feb 2009) $
                 $Revision: 4035 $
Copyright 2006 Hardcoded Software (http://www.hardcoded.net)
"""
import os
import os.path as op
import tempfile
import shutil

from hsfs import phys
from hsfs.stats import StatsList
from hsutil.conflict import is_conflicted, get_unconflicted_name
from hsutil.files import clean_empty_dirs
from hsutil.job import JobCancelled
from hsutil.misc import cond, dedupe, tryint
from hsutil.path import Path
from hsutil.str import format_size, format_time, multi_replace, FT_MINUTES, FS_FORBIDDEN

from hsutil.reg import RegistrableApplication

from . import design
from .fs_utils import Buffer, BatchOperation
from .sqlfs.music import Root, VOLTYPE_CDROM, VOLTYPE_FIXED, MODE_PHYSICAL, MODE_NORMAL

class MusicGuru(RegistrableApplication):
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
        try:
            ref = phys.music.Directory(None, path)
            self.collection.add_volume(ref, name, vol_type, job)
            return True
        except JobCancelled:
            return False
    
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
    
    def GetNodeData(self, node):
        if node.is_container:
            img_name = cond(node.allconflicts,'folder_conflict_16','folder_16')
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
            img_name = cond(is_conflicted(node.name),'song_conflict_16','song_16')
            return [
                node.name,
                node.original.parent_volume.name,
                0,
                format_size(node.size,2,2,False),
                format_time(node.duration,FT_MINUTES),
                img_name,
            ]
    
    def GetLocationData(self, location):
        return [
            location.name,
            location.get_stat('filecount'),
            format_size(location.get_stat('size'),2,3,False),
            location.vol_type == VOLTYPE_CDROM,
            location.is_available,
            unicode(location.physical_path)
        ]
    
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
    def CleanBuffer(self,dest):
        for location in self.board.locations:
            location.mode = MODE_PHYSICAL
        #Remove buffered and burned files
        to_delete = self.buffer.PurgeBufferOf(dest)
        for file in to_delete:
            source = file[0]
            source_path_str = str(source.original.path)
            if os.path.exists(source_path_str):
                os.remove(source_path_str)
        clean_empty_dirs(self.collection.buffer_path)
        for location in self.board.locations:
            location.mode = MODE_NORMAL
    
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
                    clean_empty_dirs(location.path, files_to_delete=['.DS_Store'])
                location.mode = MODE_NORMAL
            self.collection.update_volumes(job)
        except JobCancelled:
            for location in self.board.locations:
                location.mode = MODE_NORMAL
    
    def FetchSourceSongs(self,cd,job,on_need_cd):
        needed_songs = self.buffer.DoBufferingFor(cd)
        needed_sources = self.buffer.GetSources(needed_songs)
        j = job.start_subjob(len(needed_sources))
        try:
            for source in needed_sources:
                cdrom_path = on_need_cd(source)
                if not cdrom_path:
                    return
                songs_in_source = [song[0] for song in needed_songs if song[1] is source]
                j.start_job(len(songs_in_source))
                for song in songs_in_source:
                    song_path = song.original.path[2:] #remove collection name and volume
                    source_path = song_path
                    dest_path = self.collection.buffer_path + source.name + song_path
                    if not os.path.exists(str(dest_path[:-1])):
                        os.makedirs(str(dest_path[:-1]))
                    if os.path.exists(str(dest_path)):
                        continue
                    processed = False
                    while cdrom_path and (not processed):
                        try:
                            shutil.copy(str(cdrom_path + source_path),str(dest_path))
                            processed = True
                        except (OSError,IOError):
                            if os.path.exists(str(cdrom_path + source_path)):
                                processed = True
                            else:
                                cdrom_path = on_need_cd(source)
                                if not cdrom_path:
                                    return
                    j.add_progress()
        except JobCancelled:
            pass
    
    def PrepareBurning(self,free_bytes):
        buffer_dir = tempfile.mkdtemp()
        self.buffer = Buffer(int(free_bytes * 0.8))
        self.collection.buffer_path = Path(buffer_dir)
        cdroms = [l for l in self.board.locations if l.vol_type == VOLTYPE_CDROM]
        if not cdroms:
            return False
        files = []
        for song in self.board.iterallfiles():
            original = song.original
            location = original.parent_volume
            if location in cdroms:
                files.append((song,location,song.parents[1],song.size))
        self.buffer.AddFiles(files)
        return True
    
    def RenameInRespectiveLocations(self,job):
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
                clean_empty_dirs(location.path, files_to_delete=['.DS_Store'])
                location.mode = MODE_NORMAL
            self.collection.update_volumes(j)
            return 0
        except JobCancelled:
            return 2