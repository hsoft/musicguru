# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-19
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license



from PyQt4.QtCore import Qt, SIGNAL, QMimeData, QByteArray
from PyQt4.QtGui import QPixmap

from hsutil.conflict import is_conflicted
from hsutil.misc import dedupe
from hsutil.path import Path
from hsutil.str import format_size, format_time, FT_MINUTES
from qtlib.tree_model import TreeNode, TreeModel

from core.fs_utils import smart_move

MIME_PATHS = 'application/musicguru.paths'
DESIGN_BOARD_NAME = '<design board>'
IGNORE_BOX_NAME = '<ignore box>'

class FSNode(TreeNode):
    def __init__(self, model, parent, ref, row):
        TreeNode.__init__(self, model, parent, row)
        self.ref = ref
        self._data = None
        self._imageName = None
    
    def __repr__(self):
        return "<FSNode %s>" % self.ref.name
    
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
    

class DummyNode(FSNode):
    def _getData(self):
        return [''] * 5
    
    def _getImageName(self):
        return ''
    
    def _getChildren(self):
        return []
    

class FSModel(TreeModel):
    HEADER = ['Name', 'Location', 'Songs', 'Size (MB)', 'Time']
    
    def __init__(self, app, ref, name):
        self.app = app
        self.ref = ref
        self.name = name # the name is going to be the first item in the paths passed around in d&d
        TreeModel.__init__(self)
    
    def _createDummyNode(self, parent, row):
        return DummyNode(self, parent, None, row)
    
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
    
    def dropMimeData(self, mimeData, action, row, column, parentIndex):
        # In the test I have made, the row and column args always seem to be -1/-1 except when
        # parentIndex is invalid (which means that the drop destination is the root node).
        def find_path(path):
            if path[0] == DESIGN_BOARD_NAME:
                return self.app.board.find_path(path[1:])
            elif path[0] == IGNORE_BOX_NAME:
                return self.app.board.ignore_box.find_path(path[1:])
        
        if not mimeData.hasFormat(MIME_PATHS):
            return False
        if parentIndex.isValid():
            destNode = parentIndex.internalPointer()
        else:
            destNode = self
        paths = str(mimeData.data(MIME_PATHS), 'utf-8').split('\n')
        sourceItems = set(find_path(Path(path)) for path in paths)
        sourceItems = set(item for item in sourceItems if item.parent not in sourceItems | set([destNode.ref]))
        if not sourceItems:
            return False
        smart_move(sourceItems, destNode.ref, allow_merge=True)
        destNode.invalidate()
        # InsertRow calls have to be made at correct indexes or else the subsequent removeRows call
        # will be made at incorrect indexes. To do so, we just go through every subitem of destNode.ref
        # and if it's in sourceItems, we call insertRow. 
        # destNode.subnodes
        for index, node in enumerate(destNode.subnodes):
            if node.ref in sourceItems:
                self.insertRow(index, parentIndex)
        return True
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsDropEnabled
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
        if index.column() == 0:
            flags |= Qt.ItemIsEditable
        return flags
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self.HEADER):
            return self.HEADER[section]
        
        return None
    
    def insertRows(self, row, count, parentIndex):
        node = parentIndex.internalPointer() if parentIndex.isValid() else self
        self.beginInsertRows(parentIndex, row, row + count - 1)
        node.invalidate()
        self.endInsertRows()
        return True
    
    def mimeData(self, indexes):
        nodes = dedupe(index.internalPointer() for index in indexes)
        paths = [str(self.name + node.ref.path) for node in nodes]
        data = '\n'.join(paths).encode('utf-8')
        mimeData = QMimeData()
        mimeData.setData(MIME_PATHS, QByteArray(data))
        return mimeData
    
    def mimeTypes(self):
        return [MIME_PATHS]
    
    def removeRows(self, row, count, parentIndex):
        node = parentIndex.internalPointer() if parentIndex.isValid() else self
        self.beginRemoveRows(parentIndex, row, row + count - 1)
        node.invalidate()
        self.endRemoveRows()
        return True
    
    def refreshNode(self, node):
        if node is None:
            self.invalidate()
            return
        node.invalidate(with_subnodes=True)
        self.emit(SIGNAL('layoutChanged()'))
    
    def supportedDropActions(self):
        return Qt.MoveAction
    
