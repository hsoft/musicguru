# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, SIGNAL

from hsutil.misc import dedupe
from hsutil.str import format_size, format_time, FT_MINUTES
from qtlib.tree_model import TreeNode, TreeModel

class SongNode(TreeNode):
    def __init__(self, parent, song, row):
        TreeNode.__init__(self, parent, row)
        self.song = song
        self.data = [
            song.name,
            song.original.parent_volume.name,
            0,
            format_size(song.size, 2, 2, False),
            format_time(song.duration, FT_MINUTES),
        ]
    
    def _get_children(self):
        return []
    

class FolderNode(TreeNode):
    def __init__(self, parent, folder, row):
        TreeNode.__init__(self, parent, row)
        self.folder = folder
        parent_volumes = dedupe(song.original.parent_volume for song in folder.iterallfiles())
        self.data = [
            folder.name,
            ','.join(l.name for l in parent_volumes),
            folder.get_stat('filecount'),
            format_size(folder.get_stat('size'), 2, 2, False),
            format_time(folder.get_stat('duration')),
        ]
    
    def _get_children(self):
        children = []
        for index, folder in enumerate(self.folder.dirs):
            children.append(FolderNode(self, folder, index))
        offset = len(self.folder.dirs)
        for index, song in enumerate(self.folder.files):
            children.append(SongNode(self, song, index + offset))
        return children
    

class BoardModel(TreeModel):
    HEADER = ['Name', 'Location', 'Songs', 'Size (MB)', 'Time']
    
    def __init__(self, app):
        self.app = app
        self.board = app.board
        TreeModel.__init__(self)
        
        self.connect(self.app, SIGNAL('boardChanged()'), self.boardChanged)
    
    def _root_nodes(self):
        nodes = []
        for index, folder in enumerate(self.board.dirs):
            nodes.append(FolderNode(None, folder, index))
        return nodes
    
    def columnCount(self, parent):
        return len(self.HEADER)
    
    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.data[index.column()]
        return None
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self.HEADER):
            return self.HEADER[section]
        
        return None
    
    #--- Events
    def boardChanged(self):
        self.reset()
    
