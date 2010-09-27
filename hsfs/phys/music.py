# Created By: Virgil Dupras
# Created On: 2004/12/09
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from . import _phys as phys
from .. import music
from hsaudiotag import mpeg, wma, mp4, ogg, flac, aiff
from hsutil.str import get_file_ext

TAG_FIELDS = ['audiosize', 'duration', 'bitrate', 'samplerate', 'title', 'artist',
    'album', 'genre', 'year', 'track', 'comment']

class Mp3File(phys.File,music._File):
    #---Override
    def _read_info(self, field):
        if field == 'md5partial':
            fileinfo = mpeg.Mpeg(self.path)
            self._md5partial_offset = fileinfo.audio_offset
            self._md5partial_size = fileinfo.audio_size
        super(Mp3File, self)._read_info(field)
        if field in TAG_FIELDS:
            fileinfo = mpeg.Mpeg(self.path)
            self.audiosize = fileinfo.audio_size
            self.bitrate = fileinfo.bitrate
            self.duration = fileinfo.duration
            self.samplerate = fileinfo.sample_rate
            i1 = fileinfo.id3v1
            # id3v1, even when non-existant, gives empty values. not id3v2. if id3v2 don't exist,
            # just replace it with id3v1
            i2 = fileinfo.id3v2
            if not i2.exists:
                i2 = i1
            self.artist = i2.artist or i1.artist
            self.album = i2.album or i1.album
            self.title = i2.title or i1.title
            self.genre = i2.genre or i1.genre
            self.comment = i2.comment or i1.comment
            self.year = i2.year or i1.year
            self.track = i2.track or i1.track

class WmaFile(phys.File,music._File):
    #---Override
    def _read_info(self, field):
        if field == 'md5partial':
            dec = wma.WMADecoder(self.path)
            self._md5partial_offset = dec.audio_offset
            self._md5partial_size = dec.audio_size
        super(WmaFile, self)._read_info(field)
        if field in TAG_FIELDS:
            dec = wma.WMADecoder(self.path)
            self.audiosize = dec.audio_size
            self.bitrate = dec.bitrate
            self.duration = dec.duration
            self.samplerate = dec.sample_rate
            self.artist = dec.artist
            self.album = dec.album
            self.title = dec.title
            self.genre = dec.genre
            self.comment = dec.comment
            self.year = dec.year
            self.track = dec.track

class Mp4File(phys.File,music._File):
    #---Override
    def _read_info(self, field):
        if field == 'md5partial':
            dec = mp4.File(self.path)
            self._md5partial_offset = dec.audio_offset
            self._md5partial_size = dec.audio_size
            dec.close()
        super(Mp4File, self)._read_info(field)
        if field in TAG_FIELDS:
            dec = mp4.File(self.path)
            self.audiosize = dec.audio_size
            self.bitrate = dec.bitrate
            self.duration = dec.duration
            self.samplerate = dec.sample_rate
            self.artist = dec.artist
            self.album = dec.album
            self.title = dec.title
            self.genre = dec.genre
            self.comment = dec.comment
            self.year = dec.year
            self.track = dec.track
            dec.close()

class OggFile(phys.File,music._File):
    #---Override
    def _read_info(self, field):
        if field == 'md5partial':
            dec = ogg.Vorbis(self.path)
            self._md5partial_offset = dec.audio_offset
            self._md5partial_size = dec.audio_size
        super(OggFile, self)._read_info(field)
        if field in TAG_FIELDS:
            dec = ogg.Vorbis(self.path)
            self.audiosize = dec.audio_size
            self.bitrate = dec.bitrate
            self.duration = dec.duration
            self.samplerate = dec.sample_rate
            self.artist = dec.artist
            self.album = dec.album
            self.title = dec.title
            self.genre = dec.genre
            self.comment = dec.comment
            self.year = dec.year
            self.track = dec.track

class FlacFile(phys.File,music._File):
    #---Override
    def _read_info(self, field):
        if field == 'md5partial':
            dec = flac.FLAC(self.path)
            self._md5partial_offset = dec.audio_offset
            self._md5partial_size = dec.audio_size
        super(FlacFile, self)._read_info(field)
        if field in TAG_FIELDS:
            dec = flac.FLAC(self.path)
            self.audiosize = dec.audio_size
            self.bitrate = dec.bitrate
            self.duration = dec.duration
            self.samplerate = dec.sample_rate
            self.artist = dec.artist
            self.album = dec.album
            self.title = dec.title
            self.genre = dec.genre
            self.comment = dec.comment
            self.year = dec.year
            self.track = dec.track

class AiffFile(phys.File, music._File):
    #---Override
    def _read_info(self, field):
        if field == 'md5partial':
            dec = aiff.File(self.path)
            self._md5partial_offset = dec.audio_offset
            self._md5partial_size = dec.audio_size
        super(AiffFile, self)._read_info(field)
        if field in TAG_FIELDS:
            dec = aiff.File(self.path)
            self.audiosize = dec.audio_size
            self.bitrate = dec.bitrate
            self.duration = dec.duration
            self.samplerate = dec.sample_rate
            tag = dec.tag
            if tag is not None:
                self.artist = tag.artist
                self.album = tag.album
                self.title = tag.title
                self.genre = tag.genre
                self.comment = tag.comment
                self.year = tag.year
                self.track = tag.track
    

ASSOC = {
    'mp3':Mp3File,
    'wma':WmaFile,
    'm4a':Mp4File,
    'm4p':Mp4File,
    'ogg':OggFile,
    'flac':FlacFile,
    'aif':AiffFile,
    'aiff':AiffFile,
    'aifc':AiffFile,
}

class Directory(phys.Directory):
    def _create_sub_file(self, name, with_parent=True):
        parent = self if with_parent else None
        ext = get_file_ext(name)
        if ext in ASSOC:
            return ASSOC[ext](parent,name)
    
