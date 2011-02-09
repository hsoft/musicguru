# Created By: Virgil Dupras
# Created On: 2006/01/18
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os.path as op
import os
import random

from hscommon.testutil import eq_

from . import fs_utils, manualfs, design
from .sqlfs.music import Root, VOLTYPE_CDROM, VOLTYPE_FIXED
from .testcase import TestCase

class TCBoard(TestCase):
    def setUp(self):
        self.root = Root(self.filepath('sql','small.db'), threaded=False)
        self.board = design.Board()
        self.board.AddLocation(self.root[0])

    #---Locations
    def test_location_is_added(self):
        self.assert_(self.root[0] in self.board.locations)
        self.assertEqual(7,len(self.board))
        self.assertEqual('08 Peephole.wma',self.board[0].name)

    def test_location_is_read_only(self):
        self.board.locations.remove(self.root[0])
        self.assert_(self.root[0] in self.board.locations)

    def test_remove_location(self):
        self.board.RemoveLocation(self.root[0])
        self.assert_(self.root[0] not in self.board.locations)
        self.assertEqual(0,len(self.board))

    def test_remove_location_not_in_board(self):
        self.board.RemoveLocation(self.root)
        self.assertEqual(7,len(self.board))
        self.assertEqual(1,len(self.board.locations))

    def test_toggle_location(self):
        self.board.ToggleLocation(self.root[0])
        self.assert_(self.root[0] not in self.board.locations)
        self.assertEqual(0,len(self.board))
        self.board.ToggleLocation(self.root[0])
        self.assert_(self.root[0] in self.board.locations)
        self.assertEqual(7,len(self.board))

    def test_empty_dir_after_remove_location(self):
        new = self.board.new_directory('foobar')
        self.board.RemoveLocation(self.root[0])
        self.assert_(self.root[0] not in self.board.locations)
        self.assertEqual(0,len(self.board))

    def test_also_remove_from_ignore_box(self):
        self.board[0].move(self.board.ignore_box)
        self.board.RemoveLocation(self.root[0])
        self.assertEqual(0,len(self.board.ignore_box))

    #---Node Manipulation
    def test_is_auto_merge(self):
        #By testing that the board is an AutoMerge subclass, we are sure that the
        #board handles file name conflicts and automatically merge directories.
        assert isinstance(self.board, manualfs.AutoMerge)

    def test_auto_create_dir(self):
        eq_(manualfs.AutoMerge,type(self.board._create_sub_dir('foobar')))

    def test_case_insensitive(self):
        f1,f2 = self.board[:2]
        f1.name = 'foobar'
        f2.name = 'FoObAr'
        self.assertEqual('[000] FoObAr',f2.name)    

    #---High level functions
    def test_mass_rename(self):
        self.board.media_capacity = 700
        self.board.MassRename("%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        self.assertEqual('2001 - Manu_Chao - La_Primavera._Bleh.mp3',self.board[0].name)
        self.assertEqual(1,len(self.board.conflicts))
        self.assertEqual(False,self.board.splitted)
        not_renamed = self.board['(not renamed)']
        self.assertEqual(1,len(not_renamed))

    def test_that_mass_rename_priorizes(self):
        root = Root(self.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        self.board.MassRename("foobar/%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        self.assertEqual(8,len(self.board.allconflicts))
        self.assertEqual(1,len([s for s in self.board.allconflicts if s.original.parent_volume is self.board.locations[0]]))
        
    def test_mass_rename_case_insensitive(self):
        self.board[0].artist = 'foobar'
        self.board[1].artist = 'FOOBAR'
        self.board.MassRename("parent_dir/%artist%/%title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        self.assertEqual(7,len(self.board.allfiles))

    def test_empty(self):
        root = Root(self.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        self.board.media_capacity = 8500
        self.board[0].move(self.board.ignore_box)
        self.assertEqual(13,len(self.board))
        self.assertEqual(1,len(self.board.ignore_box))
        self.board.Empty()
        self.assertEqual(0,len(self.board))
        self.assertEqual(0,len(self.board.locations))
        self.assertEqual(0,len(self.board.ignore_box))
        self.assertEqual(False,self.board.splitted)

    def test_priorize_conflicts(self):
        root = Root(self.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        f1 = self.board['08 Peephole.wma']
        f2 = self.board['[000] 08 Peephole.wma']
        #Right now, the order is ok. We will switch them, and call Priorize
        f1.name = 'foobar'
        f2.name = '08 Peephole.wma'
        f1.name = '[000] 08 Peephole.wma'
        self.board.PriorizeConflicts()
        self.assertEqual('08 Peephole.wma',f1.name)
        self.assertEqual('[000] 08 Peephole.wma',f2.name)

    def test_split(self):
        self.board.Split('CD %sequence%',1,0)
        self.assertEqual(7,len(self.board.dirs))
        self.assertEqual('CD 1',self.board[0].name)
        self.assert_(self.board.splitted)
        self.board.Unsplit()

    def test_unsplit(self):
        self.board.Split('CD %sequence%', 0xffffffff, 0)
        self.assert_(self.board.splitted)
        self.board.Unsplit()
        self.assert_(not self.board.splitted)
        self.assertEqual('08 Peephole.wma',self.board[0].name)
        self.assertEqual(7, len(self.board))
    
    def test_get_stat_line(self):
        self.assertEqual("7 songs, 27.3 minutes, 34.73 MB",self.board.stats_line)
        root = Root(self.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        self.board.MassRename("foobar/%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        self.assertEqual("14 songs (8 conflicts), 54.7 minutes, 69.45 MB",self.board.stats_line)
        
    def test_stats(self):
        self.board.MassRename("%artist%\%title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        self.assertEqual(len(self.board.get_stat('artist',[])),3)
        self.assertEqual(len(self.board[1].get_stat('artist',[])),1)
        self.assertEqual(len(self.board[0].get_stat('artist',[])),1)

    #---Conflicts
    def test_move_conflicts(self):
        self.board.MassRename("%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        self.assertEqual(7,len(self.board))
        self.assertEqual(1,len(self.board.conflicts))
        self.assertEqual(1,self.board.MoveConflicts())
        self.assertEqual(6,len(self.board))
        self.assertEqual(1,len(self.board.ignore_box.allfiles))
        self.assertEqual(0,len(self.board.allconflicts))

    def test_move_conflicts_to_original(self):
        f = self.board[0]
        f.name = '[000] foobar'
        self.assertEqual(7,len(self.board))
        self.assertEqual(1,len(self.board.conflicts))
        self.assertEqual(0,self.board.MoveConflicts())
        self.assertEqual(7,len(self.board))
        self.assertEqual(0,len(self.board.ignore_box.allfiles))
        self.assertEqual(0,len(self.board.allconflicts))
        self.assertEqual('foobar',f.name)

    def test_move_conflicts_and_original(self):
        self.board.MassRename("%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        self.assertEqual(7,len(self.board))
        self.assertEqual(1,len(self.board.allconflicts))
        self.assertEqual(2,self.board.MoveConflicts(True))
        self.assertEqual(5,len(self.board))
        self.assertEqual(2,len(self.board.ignore_box.allfiles))
        self.assertEqual(0,len(self.board.allconflicts))

class TCMassRenamePanel(TestCase):
    def setUp(self):
        root = Root(self.filepath('sql','small.db'), threaded=False)
        self.panel = design.MassRenamePanel(root)

    def test_default(self):
        self.assertEqual(0,self.panel.model_index)
        self.assertEqual(0,self.panel.whitespace_index)
        self.assertEqual("%artist%/%album%/%track% - %artist% - %title%",self.panel.model)
        self.assertEqual(fs_utils.WS_DONT_TOUCH,self.panel.whitespace)

    def test_change(self):
        self.panel.model_index = 3
        self.assertEqual(3,self.panel.model_index)
        self.assertEqual("%artist%/%album% - %track% - %title%",self.panel.model)
        self.panel.whitespace_index = 2
        self.assertEqual(2,self.panel.whitespace_index)
        self.assertEqual(fs_utils.WS_UNDERSCORES_TO_SPACES,self.panel.whitespace)
        self.panel.model_index = 4
        self.assertEqual("%group:artist:emp:upper%/%artist%/%track% - %artist% - %title%",self.panel.model)
        self.panel.custom_model = 'foobar'
        self.panel.model_index = 234
        self.assertEqual("foobar",self.panel.model)

    def test_example(self):
        def mock_choice(among):
            if among:
                return among[0]

        oldchoice = random.choice
        random.choice = mock_choice
        self.assertEqual(op.join('mftest','08 Peephole.wma'),self.panel.example_before)
        self.assertEqual(op.join('Strings of SOD','String Tribute to System of a Down','08 - Strings of SOD - Peephole.wma'),self.panel.example_after)
        self.panel.refdir.clear()
        self.panel.ChangeExample()
        self.assertEqual('',self.panel.example_before)
        self.assertEqual('',self.panel.example_after)
        random.choice = oldchoice

class TCSplittingPanel(TestCase):
    def setUp(self):
        self.panel = design.SplittingPanel(manualfs.Directory(None,''))

    def test_default(self):
        self.assertEqual(0,self.panel.model_index)
        self.assertEqual(0,self.panel.capacity_index)
        self.assertEqual("CD %sequence%",self.panel.model)
        self.assertEqual(700 * 1024 * 1024,self.panel.capacity)

    def test_change(self):
        self.panel.model_index = 2
        self.assertEqual(2,self.panel.model_index)
        self.assertEqual("CD %item:first:1% - %item:last:1%",self.panel.model)
        self.panel.capacity_index = 2
        self.assertEqual(2,self.panel.capacity_index)
        self.assertEqual(8.5 * 1000 * 1000 * 1000,self.panel.capacity)
        self.panel.model_index = 4
        self.assertEqual("CD %item:first:3% - %item:last:3%",self.panel.model)
        self.panel.custom_model = 'foobar'
        self.panel.model_index = 234
        self.assertEqual("foobar",self.panel.model)

    def test_grouping(self):
        d1 = self.panel.refdir.new_directory('foo')
        d2 = d1.new_directory('bar')
        self.assertEqual('(No grouping)',self.panel.example)
        self.panel.grouping_level = 1
        self.assertEqual(os.sep + 'foo',self.panel.example)
        self.panel.grouping_level = 2
        self.assertEqual(op.join(os.sep + 'foo','bar'),self.panel.example)
        self.panel.grouping_level = 3
        self.assertEqual('(No folder at this level)',self.panel.example)
        
    def test_capacities(self):
        #The CD are really 700 mb, but the gb advertised on dvd cases are 4.7 * 1000 * 1000 * 1000 and 8.5 * 1000 * 1000 * 1000
        self.assertEqual(700 * 1024 * 1024,self.panel.capacity)
        self.panel.capacity_index = 1
        self.assertEqual(4.7 * 1000 * 1000 * 1000,self.panel.capacity)
        self.panel.capacity_index = 2
        self.assertEqual(8.5 * 1000 * 1000 * 1000,self.panel.capacity)
        self.panel.capacity_index = 3
        self.panel.custom_capacity = 42
        self.assertEqual(self.panel.capacity, 42*1024*1024)
        self.panel.capacity_index = 0
        self.assertEqual(700 * 1024 * 1024,self.panel.capacity)
