# Created By: Virgil Dupras
# Created On: 2006/08/15
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os

from py.test import importorskip
from hscommon.testutil import eq_

# This test is permanently skipped since there's no easy way to get to hsaudio's testdata now that
# the dependency is through site-package (in which testdata isn't installed) instead of through
# a subrepository.
importorskip('hsaudiotagfoobar')
from hsaudiotag.testcase import TestCase
from ..phys import music

from hscommon.util import get_file_ext

from .. import phys, _fs as fs
from ..music import _File

class TCPhysMusic(TestCase):
    def test_music(self):
        wma = music.Directory(None, self.filepath('wma'))
        eq_('Modest Mouse',wma.files[0].artist)
        mpeg = music.Directory(None, self.filepath('mpeg'))
        eq_('Alice & The Serial Numbers',mpeg['test1.mp3'].artist)
    
    # I removed test_mpeg because since the "testdata squeezing" in hsaudiotag, it failed, and it was a
    # pain to adjust this test, espcially since that kind of thing is already tested in hsaudiotag.
    
    def test_mpeg_empty_id3v2(self):
        """when id3v2 exists, but has empty values, use id3v1 values"""
        class Fake(object):pass
        m = Fake()
        m.audio_size = 42
        m.bitrate = 42
        m.duration = 42
        m.sample_rate = 42
        m.id3v1 = Fake()
        m.id3v2 = Fake()
        m.id3v1.artist = 'artist'
        m.id3v1.album = 'album'
        m.id3v1.title = 'title'
        m.id3v1.genre = 'genre'
        m.id3v1.comment = 'comment'
        m.id3v1.year = 'year'
        m.id3v1.track = 42
        m.id3v2.artist = ''
        m.id3v2.album = ''
        m.id3v2.title = ''
        m.id3v2.genre = ''
        m.id3v2.comment = ''
        m.id3v2.year = ''
        m.id3v2.track = 0
        m.id3v2.exists = True
        m.tag = m.id3v2
        self.mock(music.mpeg, 'Mpeg', lambda *a, **kw: m)
        dir = music.Directory(None, self.filepath('mpeg'))
        file = dir['test1.mp3']
        eq_(file.artist, 'artist')
        eq_(file.album, 'album')
        eq_(file.title, 'title')
        eq_(file.genre, 'genre')
        eq_(file.comment, 'comment')
        eq_(file.year, 'year')
        eq_(file.track, 42)
    
    def test_mpeg_no_tag(self):
        """Handles files with no tag correctly"""
        dir = music.Directory(None, self.filepath('mpeg'))
        file = dir['test2.mp3'] # no tag
        eq_(file.artist, '')
    
    def test_wma(self):
        dir = phys.Directory(None,self.filepath('wma'))
        file = dir['test1.wma']
        #size = 0x582682 audio-offset = 0x158c audio-size = 0x5810f6
        file._md5partial_offset = 0x15a0
        file._md5partial_size = 0x582682 - 0x15a0
        refmd5 = file.md5partial
        dir = music.Directory(None,self.filepath('wma'))
        file = dir['test1.wma']
        eq_(refmd5,file.md5partial)
        eq_(0x582682 - 0x15a0,file.audiosize)
        eq_(44100,file.samplerate)
    
    def test_mp4(self):
        dir = phys.Directory(None,self.filepath('mp4'))
        file = dir['test1.m4a']
        #size = 0x3357ad audio-offset = 0xc820 audio-size = 0x328f8d
        file._md5partial_offset = 0xc820
        file._md5partial_size = 0x328f8d
        refmd5 = file.md5partial
        dir = music.Directory(None,self.filepath('mp4'))
        file = dir['test1.m4a']
        eq_(refmd5,file.md5partial)
        eq_(0x328f8d,file.audiosize)
        eq_(44100,file.samplerate)
    
    def test_ogg(self):
        dir = phys.Directory(None,self.filepath('ogg'))
        file = dir['test1.ogg']
        #size = 0x2f5440 audio-offset = 0x1158 audio-size = 0x2f42e8
        file._md5partial_offset = 0x1158
        file._md5partial_size = 97345
        refmd5 = file.md5partial
        dir = music.Directory(None,self.filepath('ogg'))
        file = dir['test1.ogg']
        eq_(refmd5,file.md5partial)
        eq_(101785, file.size)
        eq_(160, file.bitrate)
        eq_(162, file.duration)
        eq_(44100, file.samplerate)
        eq_('The White Stripes', file.artist)
        eq_('The White Stripes', file.album)
        eq_('Astro', file.title)
        eq_('', file.genre)
        eq_('', file.comment)
        eq_('1999', file.year)
        eq_(8, file.track)
        eq_(97345, file.audiosize)
    
    def test_flac(self):
        dir = phys.Directory(None, self.filepath('flac'))
        file = dir['test1.flac']
        #size = 0x10cea29 audio-offset = 0x1190 audio-size = 0x10cd899
        file._md5partial_offset = 0x1190
        file._md5partial_size = 119123
        refmd5 = file.md5partial
        dir = music.Directory(None, self.filepath('flac'))
        file = dir['test1.flac']
        eq_(refmd5,file.md5partial)
        eq_(123619, file.size)
        eq_(0, file.bitrate)
        eq_(177, file.duration)
        eq_(44100, file.samplerate)
        eq_('Coolio', file.artist)
        eq_('it takes a thief', file.album)
        eq_('Country Line', file.title)
        eq_('Hip-Hop', file.genre)
        eq_('It sucks', file.comment)
        eq_('1994', file.year)
        eq_(2, file.track)
        eq_(119123, file.audiosize)
    
    def test_aiff(self):
        dir = phys.Directory(None, self.filepath('aiff'))
        file = dir['with_id3.aif']
        #size = 2292 audio-offset = 46 audio-size = 42
        file._md5partial_offset = 46
        file._md5partial_size = 42
        refmd5 = file.md5partial
        dir = music.Directory(None, self.filepath('aiff'))
        file = dir['with_id3.aif']
        eq_(refmd5, file.md5partial)
        eq_(2292, file.size)
        eq_(1411200, file.bitrate)
        eq_(132, file.duration)
        eq_(44100, file.samplerate)
        eq_('Assimil', file.artist)
        eq_('Assimil Polonais 4', file.album)
        eq_('Piste 100 Jezyki obce', file.title)
        eq_('Books & Spoken', file.genre)
        eq_('', file.year)
        eq_(20, file.track)
        eq_(42, file.audiosize)
    
    def test_filecount(self):
        #With the performance changes fs.auto got, when filecount was called
        #before the cache was built, non-music files were included in the 
        #count too.
        d = music.Directory(None,self.filepath('mpeg'))
        content = os.listdir(self.filepath('mpeg'))
        mpeg_count = len([name for name in content if get_file_ext(name) == 'mp3'])
        eq_(mpeg_count,d.filecount)
    
