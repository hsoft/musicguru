# Created By: Virgil Dupras
# Created On: 2006/01/18
# $Id$
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import random

from hsutil import job, conflict
from hsutil.str import pluralize, format_size, format_time, FT_DECIMAL

from . import fs_utils, manualfs

class Board(manualfs.AutoMerge):
    cls_dir_class = manualfs.AutoMerge

    def __init__(self):
        super(Board,self).__init__(None,'')
        self.case_sensitive = False
        self.__locations = []
        self.ignore_box = manualfs.AutoMerge(None,'')
        self.media_capacity = 0

    #---Private
    def __GetStatsLine(self):
        if self.allconflicts:
            return "%s (%d conflicts), %s, %s" % (
                pluralize(self.get_stat('filecount'), 'song'),
                len(self.allconflicts),
                format_time(self.get_stat('duration'), FT_DECIMAL),
                format_size(self.get_stat('size'), 2))
        else:
            return "%s, %s, %s" % (
                pluralize(self.get_stat('filecount'), 'song'),
                format_time(self.get_stat('duration'), FT_DECIMAL),
                format_size(self.get_stat('size'), 2))

    #---Public
    def AddLocation(self,location):
        if location not in self.__locations:
            self.copy(location)
            self.__locations.append(location)
            return True

    def Empty(self):
        self.clear()
        self.__locations = []
        self.ignore_box.clear()
        self.media_capacity = 0

    def MassRename(self,model,whitespace,parent_job=job.nulljob):
        renamed = fs_utils.RestructureDirectory(self,model,whitespace,False,False,parent_job)
        self.clear()
        self.copy(renamed)
        self.detach_copy(True)
        self.PriorizeConflicts()
        self.media_capacity = 0

    def MoveConflicts(self,with_original = False):
        def do_move(song):
            dest_path = 'conflicts' + song.path[1:-1]
            dest = self.ignore_box.add_path(dest_path)
            song.move(dest, conflict.get_conflicted_name(dest,song.name))

        result = 0
        for song in self.allconflicts:
            try:
                original = song.parent[conflict.get_unconflicted_name(song.name)]
            except KeyError:
                original = None
            if with_original:
                do_move(song)
                result += 1
                if original is not None:
                    do_move(original)
                    result += 1
            else:
                if original is not None:
                    do_move(song)
                    result += 1
                else:
                    song.name = conflict.get_unconflicted_name(song.name)
        return result

    def PriorizeConflicts(self):
        #Go through all conflicts and see if their original has a lower priority than theirs
        #If yes, switch them.
        for file in self.allconflicts:
            original_name = conflict.get_unconflicted_name(file.name)
            try:
                original = file.parent[original_name]
                if self.locations.index(original.original.parent_volume) > self.locations.index(file.original.parent_volume):
                    #original has a lower priority
                    old_name = file.name
                    original.name = '__switching__'
                    file.name = original_name
                    original.name = old_name
            except KeyError:
                file.name = original_name

    def RemoveLocation(self,location):
        try:
            self.__locations.remove(location)
            for file in (f for f in self.allfiles if location in f.original.parents):
                file.delete()
            self.clean_empty_dirs()
            for file in (f for f in self.ignore_box.allfiles if location in f.original.parents):
                file.delete()
            self.ignore_box.clean_empty_dirs()
            return True
        except ValueError:
            pass

    def Split(self, model, capacity, grouping_level, parent_job=job.nulljob):
        self.media_capacity = capacity
        splitted = fs_utils.Split(self,model,capacity,grouping_level)
        self.clear()
        self.copy(splitted)
        self.detach_copy(True)
    
    def ToggleLocation(self,location):
        if not self.RemoveLocation(location):
            self.AddLocation(location)

    def Unsplit(self):
        cds = self.dirs
        for cd in cds:
            cd.parent = None
        for cd in cds:
            for item in cd[:]:
                item.move(self)
        self.media_capacity = 0
        self.PriorizeConflicts()

    locations  = property(lambda x:x.__locations[:])
    splitted   = property(lambda x:x.media_capacity > 0)
    stats_line = property(__GetStatsLine)

class MassRenamePanel(object):
    WHITESPACES = [fs_utils.WS_DONT_TOUCH, fs_utils.WS_SPACES_TO_UNDERSCORES, fs_utils.WS_UNDERSCORES_TO_SPACES]
    MODELS = [
        "%artist%/%album%/%track% - %artist% - %title%",
        "%artist%/%album%/%track% - %title%",
        "%genre%/%artist%/(%year%) %album%/%track% - %title%",
        "%artist%/%album% - %track% - %title%",
    ]
    
    def __init__(self,refdir):
        self.custom_model = "%group:artist:emp:upper%/%artist%/%track% - %artist% - %title%"
        self.model_index = 0
        self.whitespace_index = 0
        self.refdir = refdir
        self.example = None
    
    #--- Public
    def ChangeExample(self):
        self.example = random.choice(self.refdir.allfiles)
    
    #--- Properties
    @property
    def example_after(self):
        if self.example is None:
            self.ChangeExample()
        if self.example is None:
            return ''
        tmp = manualfs.Directory(None,'')
        tmp.add_file_copy(self.example)
        renamed = fs_utils.RestructureDirectory(tmp,self.model,self.whitespace)
        file = renamed.allfiles[0]
        return unicode(file.path[1:])
    
    @property
    def example_before(self):
        if self.example is None:
            self.ChangeExample()
        if self.example is None:
            return ''
        return unicode(self.example.path[1:])
    
    @property
    def model(self):
        try:
            return self.MODELS[self.model_index]
        except IndexError:
            return self.custom_model.replace('\\','/')
    
    @property
    def whitespace(self):
        try:
            return self.WHITESPACES[self.whitespace_index]
        except IndexError:
            return fs_utils.WS_DONT_TOUCH
    

class SplittingPanel(object):
    CAPACITIES = [700*1024*1024, 4700*1000*1000, 8500*1000*1000]
    MODELS = ["CD %sequence%", "CD %item:first% - %item:last%", "CD %item:first:1% - %item:last:1%"]
    
    def __init__(self,refdir):
        self.custom_model = "CD %item:first:3% - %item:last:3%"
        self.model_index = 0
        self.capacity_index = 0
        self.grouping_level = 0
        self.custom_capacity = 650
        self.refdir = refdir
    
    #--- Properties
    @property
    def example(self):
        if self.grouping_level == 0:
            return '(No grouping)'
        sample = [d for d in self.refdir.alldirs if len(list(d.parents)) == self.grouping_level]
        if sample:
            example = random.choice(sample)
            return unicode(example.path)
        else:
            return '(No folder at this level)'
    
    @property    
    def model(self):
        try:
            return self.MODELS[self.model_index]
        except IndexError:
            return self.custom_model.replace('\\','/')
    
    @property
    def capacity(self):
        try:
            return self.CAPACITIES[self.capacity_index]
        except IndexError:
            return self.custom_capacity * 1024 * 1024
