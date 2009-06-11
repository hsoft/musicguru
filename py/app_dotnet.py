#!/usr/bin/env python
"""
Unit Name: musicguru.app
Created By: Virgil Dupras
Created On: 2006/11/18
Last modified by:$Author: hsoft $
Last modified on:$Date: 2006-11-18 15:47:29 -0500 (Sat, 18 Nov 2006) $
                 $Revision: 1662 $
Copyright 2006 Hardcoded Software (http://www.hardcoded.net)
"""
import os.path as op
import sys

from hsutil import job

from .import app, design

class MusicGuru(app.MusicGuru):
    def __init__(self,appdata=None):
        super(MusicGuru, self).__init__(appdata)
        sys.stdout = open(op.join(self.appdata,'debug.log'),'a')
        sys.stderr = sys.stdout
    
    def AddLocation(self,path,name,removeable,callback):
        return super(MusicGuru,self).AddLocation(path,name,removeable,job.Job(1, callback))
        
    def GetMassRenamePanel(self):
        return design.MassRenamePanel(self.board)
        
    def GetSplitPanel(self):
        return design.SplittingPanel(self.board)
        
    def MassRename(self,model,whitespace,callback):
        try:
            self.board.MassRename(model,whitespace,job.Job(1, callback))
        except job.JobCancelled:
            pass
        
    def Split(self,model,capacity,grouping_level,truncate_name_to,callback):
        try:
            self.board.Split(model,capacity,grouping_level,truncate_name_to,job.Job(1, callback))
        except job.JobCancelled:
            pass
        
    def UpdateCollection(self,callback):
        try:
            self.collection.update_volumes(job.Job(1, callback))
        except job.JobCancelled:
            pass
    
    def UpdateVolume(self, volume, callback):
        try:
            volume.update(job=job.Job(1, callback))
        except job.JobCancelled:
            pass
    
    #---Materialize
    def CopyOrMove(self,copy,destination,callback,need_cd_callback):
        def on_need_cd(location):
            return need_cd_callback(location.name)
        
        super(MusicGuru,self).CopyOrMove(copy,destination,job.Job(1, callback),on_need_cd)
    
    def FetchSourceSongs(self,cd,callback,need_cd_callback):
        def on_need_cd(location):
            return need_cd_callback(location.name)
        
        super(MusicGuru,self).FetchSourceSongs(cd,job.Job(1, callback),on_need_cd)
    
    def RenameInRespectiveLocations(self,callback):
        return super(MusicGuru,self).RenameInRespectiveLocations(job.Job(1, callback))