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
from PyQt4.QtGui import QPixmap

from hsutil.conflict import is_conflicted
from hsutil.misc import dedupe
from hsutil.str import format_size, format_time, FT_MINUTES
from qtlib.tree_model import TreeNode, TreeModel

class FSNode(TreeNode):
    def __init__(self, parent, ref, row):
        TreeNode.__init__(self, parent, row)
        self.ref = ref
        self._data = None
        self._imageName = None
    
    def _getData(self):
        raise NotImplementedError()
    
    def _getImageName(self):
        raise NotImplementedError()
    
    def reset(self):
        self._data = None
        self._imageName = None
    
    @property
    def data(self):
        if self._data is None:
            self._data = self._getData()
        return self._data
    
    @property
    def imageName(self):
        if self._imageName is None:
            self._imageName = self._getImageName()
        return self._imageName
    

class SongNode(FSNode):
    def _getData(self):
        song = self.ref
        return [
            song.name,
            song.original.parent_volume.name,
            0,
            format_size(song.size, 2, 2, False),
            format_time(song.duration, FT_MINUTES),
        ]
    
    def _getImageName(self):
        return 'song_conflict' if is_conflicted(self.ref.name) else 'song'
    
    def _get_children(self):
        return []
    

class FolderNode(FSNode):
    def _getData(self):
        folder = self.ref
        parent_volumes = dedupe(song.original.parent_volume for song in folder.iterallfiles())
        return [
            folder.name,
            ','.join(l.name for l in parent_volumes),
            folder.get_stat('filecount'),
            format_size(folder.get_stat('size'), 2, 2, False),
            format_time(folder.get_stat('duration')),
        ]
    
    def _getImageName(self):
        return 'folder_conflict' if self.ref.allconflicts else 'folder'
    
    def _get_children(self):
        children = []
        for index, folder in enumerate(self.ref.dirs):
            children.append(FolderNode(self, folder, index))
        offset = len(self.ref.dirs)
        for index, song in enumerate(self.ref.files):
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
        elif role == Qt.DecorationRole:
            if index.column() == 0:
                return QPixmap(":/{0}".format(node.imageName))
        elif role == Qt.EditRole:
            if index.column() == 0:
                return node.data[index.column()]
        return None
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 0:
            flags |= Qt.ItemIsEditable
        return flags
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self.HEADER):
            return self.HEADER[section]
        
        return None
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        node = index.internalPointer()
        if role == Qt.EditRole:
            if index.column() == 0:
                value = unicode(value.toString())
                self.app.RenameNode(node.ref, value)
                node.reset()
                return True
        return False
    
    #--- Events
    def boardChanged(self):
        self.reset()
    
