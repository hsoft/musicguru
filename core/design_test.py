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
from .sqlfs.music import Root
from .testutil import testdata

class TestBoard:
    def setup_method(self, method):
        self.root = Root(testdata.filepath('sql','small.db'), threaded=False)
        self.board = design.Board()
        self.board.AddLocation(self.root[0])

    #---Locations
    def test_location_is_added(self):
        assert self.root[0] in self.board.locations
        eq_(7,len(self.board))
        eq_('08 Peephole.wma',self.board[0].name)

    def test_location_is_read_only(self):
        self.board.locations.remove(self.root[0])
        assert self.root[0] in self.board.locations

    def test_remove_location(self):
        self.board.RemoveLocation(self.root[0])
        assert self.root[0] not in self.board.locations
        eq_(0,len(self.board))

    def test_remove_location_not_in_board(self):
        self.board.RemoveLocation(self.root)
        eq_(7,len(self.board))
        eq_(1,len(self.board.locations))

    def test_toggle_location(self):
        self.board.ToggleLocation(self.root[0])
        assert self.root[0] not in self.board.locations
        eq_(0,len(self.board))
        self.board.ToggleLocation(self.root[0])
        assert self.root[0] in self.board.locations
        eq_(7,len(self.board))

    def test_empty_dir_after_remove_location(self):
        new = self.board.new_directory('foobar')
        self.board.RemoveLocation(self.root[0])
        assert self.root[0] not in self.board.locations
        eq_(0,len(self.board))

    def test_also_remove_from_ignore_box(self):
        self.board[0].move(self.board.ignore_box)
        self.board.RemoveLocation(self.root[0])
        eq_(0,len(self.board.ignore_box))

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
        eq_('[000] FoObAr',f2.name)    

    #---High level functions
    def test_mass_rename(self):
        self.board.media_capacity = 700
        self.board.MassRename("%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        eq_('2001 - Manu_Chao - La_Primavera._Bleh.mp3',self.board[0].name)
        eq_(1,len(self.board.conflicts))
        eq_(False,self.board.splitted)
        not_renamed = self.board['(not renamed)']
        eq_(1,len(not_renamed))

    def test_that_mass_rename_priorizes(self):
        root = Root(testdata.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        self.board.MassRename("foobar/%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        eq_(8,len(self.board.allconflicts))
        eq_(1,len([s for s in self.board.allconflicts if s.original.parent_volume is self.board.locations[0]]))
        
    def test_mass_rename_case_insensitive(self):
        self.board[0].artist = 'foobar'
        self.board[1].artist = 'FOOBAR'
        self.board.MassRename("parent_dir/%artist%/%title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        eq_(7,len(self.board.allfiles))

    def test_empty(self):
        root = Root(testdata.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        self.board.media_capacity = 8500
        self.board[0].move(self.board.ignore_box)
        eq_(13,len(self.board))
        eq_(1,len(self.board.ignore_box))
        self.board.Empty()
        eq_(0,len(self.board))
        eq_(0,len(self.board.locations))
        eq_(0,len(self.board.ignore_box))
        eq_(False,self.board.splitted)

    def test_priorize_conflicts(self):
        root = Root(testdata.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        f1 = self.board['08 Peephole.wma']
        f2 = self.board['[000] 08 Peephole.wma']
        #Right now, the order is ok. We will switch them, and call Priorize
        f1.name = 'foobar'
        f2.name = '08 Peephole.wma'
        f1.name = '[000] 08 Peephole.wma'
        self.board.PriorizeConflicts()
        eq_('08 Peephole.wma',f1.name)
        eq_('[000] 08 Peephole.wma',f2.name)

    def test_split(self):
        self.board.Split('CD %sequence%',1,0)
        eq_(7,len(self.board.dirs))
        eq_('CD 1',self.board[0].name)
        assert self.board.splitted
        self.board.Unsplit()

    def test_unsplit(self):
        self.board.Split('CD %sequence%', 0xffffffff, 0)
        assert self.board.splitted
        self.board.Unsplit()
        assert not self.board.splitted
        eq_('08 Peephole.wma',self.board[0].name)
        eq_(7, len(self.board))
    
    def test_get_stat_line(self):
        eq_("7 songs, 27.3 minutes, 34.73 MB",self.board.stats_line)
        root = Root(testdata.filepath('sql','small.db'), threaded=False)
        self.board.AddLocation(root[0])
        self.board.MassRename("foobar/%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        eq_("14 songs (8 conflicts), 54.7 minutes, 69.45 MB",self.board.stats_line)
        
    def test_stats(self):
        self.board.MassRename("%artist%\%title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        eq_(len(self.board.get_stat('artist',[])),3)
        eq_(len(self.board[1].get_stat('artist',[])),1)
        eq_(len(self.board[0].get_stat('artist',[])),1)

    #---Conflicts
    def test_move_conflicts(self):
        self.board.MassRename("%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        eq_(7,len(self.board))
        eq_(1,len(self.board.conflicts))
        eq_(1,self.board.MoveConflicts())
        eq_(6,len(self.board))
        eq_(1,len(self.board.ignore_box.allfiles))
        eq_(0,len(self.board.allconflicts))

    def test_move_conflicts_to_original(self):
        f = self.board[0]
        f.name = '[000] foobar'
        eq_(7,len(self.board))
        eq_(1,len(self.board.conflicts))
        eq_(0,self.board.MoveConflicts())
        eq_(7,len(self.board))
        eq_(0,len(self.board.ignore_box.allfiles))
        eq_(0,len(self.board.allconflicts))
        eq_('foobar',f.name)

    def test_move_conflicts_and_original(self):
        self.board.MassRename("%year% - %artist% - %title%",fs_utils.WS_SPACES_TO_UNDERSCORES)
        eq_(7,len(self.board))
        eq_(1,len(self.board.allconflicts))
        eq_(2,self.board.MoveConflicts(True))
        eq_(5,len(self.board))
        eq_(2,len(self.board.ignore_box.allfiles))
        eq_(0,len(self.board.allconflicts))

class TestMassRenamePanel:
    def setup_method(self, method):
        root = Root(testdata.filepath('sql','small.db'), threaded=False)
        self.panel = design.MassRenamePanel(root)

    def test_default(self):
        eq_(0,self.panel.model_index)
        eq_(0,self.panel.whitespace_index)
        eq_("%artist%/%album%/%track% - %artist% - %title%",self.panel.model)
        eq_(fs_utils.WS_DONT_TOUCH,self.panel.whitespace)

    def test_change(self):
        self.panel.model_index = 3
        eq_(3,self.panel.model_index)
        eq_("%artist%/%album% - %track% - %title%",self.panel.model)
        self.panel.whitespace_index = 2
        eq_(2,self.panel.whitespace_index)
        eq_(fs_utils.WS_UNDERSCORES_TO_SPACES,self.panel.whitespace)
        self.panel.model_index = 4
        eq_("%group:artist:emp:upper%/%artist%/%track% - %artist% - %title%",self.panel.model)
        self.panel.custom_model = 'foobar'
        self.panel.model_index = 234
        eq_("foobar",self.panel.model)

    def test_example(self):
        def mock_choice(among):
            if among:
                return among[0]

        oldchoice = random.choice
        random.choice = mock_choice
        eq_(op.join('mftest','08 Peephole.wma'),self.panel.example_before)
        eq_(op.join('Strings of SOD','String Tribute to System of a Down','08 - Strings of SOD - Peephole.wma'),self.panel.example_after)
        self.panel.refdir.clear()
        self.panel.ChangeExample()
        eq_('',self.panel.example_before)
        eq_('',self.panel.example_after)
        random.choice = oldchoice

class TestSplittingPanel:
    def setup_method(self, method):
        self.panel = design.SplittingPanel(manualfs.Directory(None,''))

    def test_default(self):
        eq_(0,self.panel.model_index)
        eq_(0,self.panel.capacity_index)
        eq_("CD %sequence%",self.panel.model)
        eq_(700 * 1024 * 1024,self.panel.capacity)

    def test_change(self):
        self.panel.model_index = 2
        eq_(2,self.panel.model_index)
        eq_("CD %item:first:1% - %item:last:1%",self.panel.model)
        self.panel.capacity_index = 2
        eq_(2,self.panel.capacity_index)
        eq_(8.5 * 1000 * 1000 * 1000,self.panel.capacity)
        self.panel.model_index = 4
        eq_("CD %item:first:3% - %item:last:3%",self.panel.model)
        self.panel.custom_model = 'foobar'
        self.panel.model_index = 234
        eq_("foobar",self.panel.model)

    def test_grouping(self):
        d1 = self.panel.refdir.new_directory('foo')
        d2 = d1.new_directory('bar')
        eq_('(No grouping)',self.panel.example)
        self.panel.grouping_level = 1
        eq_(os.sep + 'foo',self.panel.example)
        self.panel.grouping_level = 2
        eq_(op.join(os.sep + 'foo','bar'),self.panel.example)
        self.panel.grouping_level = 3
        eq_('(No folder at this level)',self.panel.example)
        
    def test_capacities(self):
        #The CD are really 700 mb, but the gb advertised on dvd cases are 4.7 * 1000 * 1000 * 1000 and 8.5 * 1000 * 1000 * 1000
        eq_(700 * 1024 * 1024,self.panel.capacity)
        self.panel.capacity_index = 1
        eq_(4.7 * 1000 * 1000 * 1000,self.panel.capacity)
        self.panel.capacity_index = 2
        eq_(8.5 * 1000 * 1000 * 1000,self.panel.capacity)
        self.panel.capacity_index = 3
        self.panel.custom_capacity = 42
        eq_(self.panel.capacity, 42*1024*1024)
        self.panel.capacity_index = 0
        eq_(700 * 1024 * 1024,self.panel.capacity)
