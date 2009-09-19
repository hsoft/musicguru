# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-19
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
    def __init__(self, model, parent, ref, row):
        TreeNode.__init__(self, model, parent, row)
        self.ref = ref
        self._data = None
        self._imageName = None
    
    def _getData(self):
        raise NotImplementedError()
    
    def _getImageName(self):
        raise NotImplementedError()
    
    def invalidate(self, with_subnodes=False):
        if with_subnodes:
            for node in self.subnodes:
                node.invalidate(with_subnodes=True)
        self._data = None
        self._imageName = None
        TreeNode.invalidate(self)
    
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
    
    def _getChildren(self):
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
    
    def _createNode(self, ref, row):
        if ref.is_container:
            return FolderNode(self.model, self, ref, row)
        else:
            return SongNode(self.model, self, ref, row)
    
    def _getChildren(self):
        return self.ref.dirs + self.ref.files
    

class FSModel(TreeModel):
    HEADER = ['Name', 'Location', 'Songs', 'Size (MB)', 'Time']
    
    def __init__(self, ref):
        self.ref = ref
        TreeModel.__init__(self)
    
    def _createNode(self, ref, row):
        if ref.is_container:
            return FolderNode(self, None, ref, row)
        else:
            return SongNode(self, None, ref, row)
    
    def _getChildren(self):
        return self.ref.dirs
    
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
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self.HEADER):
            return self.HEADER[section]
        
        return None
    
    def refreshNode(self, node):
        if node is None:
            self.invalidate()
            return
        node.invalidate(with_subnodes=True)
        self.emit(SIGNAL('layoutChanged()'))
    
