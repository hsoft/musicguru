# Created By: Virgil Dupras
# Created On: 2005/09/08
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import tempfile

import hsfs as fs
from hsutil import conflict, io
from hsutil.misc import tryint, dedupe
from hsutil.path import Path
from hsutil.str import multi_replace, FS_FORBIDDEN, rem_file_ext, process_tokens
from hscommon.job import nulljob, JobCancelled

from .sqlfs.music import VOLTYPE_CDROM, MODE_TOKEN, MODE_NORMAL
from .manualfs import AutoResolve

(WS_DONT_TOUCH,
 WS_SPACES_TO_UNDERSCORES,
 WS_UNDERSCORES_TO_SPACES) = list(range(3))
 
def smart_move(items, dest, allow_merge=True):
    """move items into dest by taking care of name conflicts.
    
    It is assumed that every item has an assigned parent.
    Don't include root items in items.
    """
    items = [item for item in items if item.parent not in items]
    for item in [item for item in items if item not in dest]:
        try:
            item.move(dest)
        except fs.AlreadyExistsError:
            merged = False
            if allow_merge:
                dest_item = dest[item.name]
                if dest_item.is_container and item.is_container:
                    smart_move(item, dest_item, True)
                    merged = True
            if not merged:
                item_name = conflict.get_unconflicted_name(item.name)
                item.move(dest, conflict.get_conflicted_name(dest, item_name))

def RestructureDirectory(directory, namingmodel, whitespaces=WS_DONT_TOUCH, case_sensitive=True, rename_empty_tag=True, parent_job=nulljob):
    def do_process(s, clean=True):
        if clean:
            s = multi_replace(s, FS_FORBIDDEN, ' ')
        if whitespaces == WS_SPACES_TO_UNDERSCORES:
            return s.replace(' ', '_').replace('\t', '_')
        elif whitespaces == WS_UNDERSCORES_TO_SPACES:
            return s.replace('_', ' ')
        else:
            return s
    
    def handle_group(song, attr, steps='emp', case='upper'):
        if not hasattr(song, attr):
            return
        attr = getattr(song, attr)
        steps = 'a' + steps.lower() + chr(ord('z') + 1)
        letter = attr[:1].lower()
        if not letter:
            letter = 'a'
        result = 0
        for i in range(len(steps) - 1):
            start = steps[i]
            end = steps[i+1]
            if ord(letter) in range(ord(start), ord(end)):
                result = i
                break
        result = '%s-%s' % (steps[result], chr(ord(steps[result + 1]) - 1))
        if case == 'upper':
            result = result.upper()
        return result
    
    def handle_firstletter(song, attr, case='upper'):
        if not hasattr(song, attr):
            return
        attr = getattr(song, attr)
        if not attr:
            return
        result = attr[:1]
        if case == 'upper':
            result = result.upper()
        else:
            result = result.lower()
        return result
    
    handlers = {
        'artist'   : lambda d: do_process(d.artist),
        'album'    : lambda d: do_process(d.album),
        'year'     : lambda d: do_process(str(d.year)),
        'genre'    : lambda d: do_process(d.genre),
        'track'    : lambda d: do_process('%02d' % d.track, False),
        'title'    : lambda d: do_process(d.title),
        'extension': lambda d: do_process(d.extension),
        'oldpath'  : lambda d: do_process(str(d.parent.path), False),
        'oldfilename': lambda d: do_process(rem_file_ext(d.name)),
        'group'    : handle_group,
        'firstletter': handle_firstletter,
    }
    namingmodel = namingmodel.replace('\\', '/')
    result = AutoResolve(None, '')
    if not case_sensitive:
        result.case_sensitive = False
    files = directory.allfiles
    parent_job.start_job(len(files))
    for song in files:
        new_path_str = process_tokens(namingmodel, handlers, song)
        if song.extension:
            new_path_str = "%s.%s" % (new_path_str, song.extension)
        if (not rename_empty_tag) and ('(none)' in new_path_str):
            new_path = (('(not renamed)',) + song.path)
        else:
            new_path = Path(new_path_str)
        folder_path = new_path[:-1]
        folder = result.add_path(folder_path)
        folder.add_file_copy(song, new_path[-1])
        parent_job.add_progress()
    return result

def Split(refdir, naming_model, max_bytes, grouping_level=0):
    """Splits 'refdir' in chunks of 'max_bytes'.
    
    refdir: The directory to split
    naming_model: Naming model for the CDs ONLY
    max_bytes: the maximum number of bytes that can go in a CD
    grouping_level: 0 if you don't want to group. >0 if you want to group
                    The grouping level correspond to the level of directory
                    where Split will start to move directories in bulk
                    The expression to know if a directory represents a group is
                    grouping_level == len(refdir.parents)
    """
    def rename_chunks():
        def handle_item(chunk, which, letter=0):
            if not len(chunk):
                return
            if which == 'first':
                result = chunk[0].name
            elif which == 'last':
                result = chunk[-1].name
            if letter:
                result = result[:tryint(letter, None)]
            result = multi_replace(result, FS_FORBIDDEN, ' ')
            return result
        
        def handle_sequence(chunk, digits='0'):
            try:
                digits = int(digits)
            except ValueError:
                digits = 0
            model = "%%0%dd" % digits
            return model % (seq)
        
        handlers = {
            'sequence' : handle_sequence,
            'item'     : handle_item,
        }
        seq = 0
        for chunk in result:
            seq += 1
            chunk.name = process_tokens(naming_model, handlers, chunk)
    
    def get_item_dest(item, size):
        chunk = result[-1]
        cumul_size = chunk.cumul_size
        if (cumul_size > 0) and (cumul_size + size > max_bytes):
            chunk = result.new_directory(str(len(result)))
            chunk.cumul_size = 0
        chunk.cumul_size += size
        return chunk.add_path(item.path[1:-1])
    
    def split_directory(directory):
        size = directory.get_stat('size')
        if (grouping_level > 0) and (len(list(directory.parents)) >= grouping_level) and (size <= max_bytes):
            dest = get_item_dest(directory, size)
            dest.add_dir_copy(directory)
        else:
            for subfile in directory.files:
                size = subfile.size
                dest = get_item_dest(subfile, size)
                dest.add_file_copy(subfile)
            for subdir in directory.dirs:
                split_directory(subdir)
    
    result = AutoResolve(None, '')
    result.new_directory('0').cumul_size = 0
    split_directory(refdir)
    rename_chunks()
    return result

class BatchOperation(object):
    #---Override
    def __init__(self, renamed, destination):
        """renamed can be any iterable containing songs, or a Directory.
        destination: a Path that represents the directory to move files to.

        name_list is set on init. It is a list of tuples.
        Each tuple being 2 items long (source, dest).
        The first element of path in songs from 'renamed' is cut.
        """
        if isinstance(renamed, fs.Directory):
            renamed = renamed.allfiles
        destination = Path(destination)
        self.renamed = renamed
        self.destination = destination
        cd_locations = []
        for song in renamed:
            original = song.original
            try:
                volume = original.parent_volume
                if (volume.vol_type == VOLTYPE_CDROM) and (volume not in cd_locations):
                    cd_locations.append(volume)
            except AttributeError:
                pass
        self.cd_locations = cd_locations
        for location in cd_locations:
            location.mode = MODE_TOKEN
        source_paths = [song.original.path for song in renamed]
        dest_paths = [destination + song.path[1:] for song in renamed]
        self.name_list = [t for t in zip(source_paths, dest_paths) if t[0] != t[1]]
        for location in cd_locations:
            location.mode = MODE_NORMAL

    #---Private
    def __Perform(self, copy=False, job=nulljob):
        try:
            cd_operations = [t for t in self.name_list if t[0][0].startswith('!')]
            normal_operations = [t for t in self.name_list if t not in cd_operations]
            cds = dedupe(t[0][0][1:] for t in cd_operations)
            job_count = len(cds)
            if normal_operations:
                job_count += 1
            newjob = job.start_subjob(job_count)
            if normal_operations:
                self.__ProcessNormalList(normal_operations, copy, newjob)
            for cd in cds:
                cd_location = [location for location in self.cd_locations if location.name == cd][0]
                cd_path = self.OnNeedCD(cd_location)
                if not cd_path:
                    return False
                name_list = [(t[0][1:], t[1]) for t in cd_operations if t[0][0][1:] == cd]
                if not self.__ProcessCDList(name_list, Path(cd_path), cd_location, newjob):
                    return False
            return True
        except JobCancelled:
            return False

    def __ProcessCDList(self, name_list, cd_path, cd_location, job=nulljob):
        job.start_job(len(name_list))
        for source, dest in name_list:
            if not io.exists(dest[:-1]):
                io.makedirs(dest[:-1])
            if not io.exists(dest):
                processed = False
                while cd_path and (not processed):
                    try:
                        io.copy((cd_path + source), dest)
                        processed = True
                    except (OSError, IOError):
                        if io.exists(cd_path + source):
                            processed = True
                            #This is a very special case. It happens when the path on the
                            #CD is too long to be copied. It very seldom happens. Just skip the file.
                        else:
                            cd_path = self.OnNeedCD(cd_location)
                            if cd_path:
                                cd_path = Path(cd_path)
                            else:
                                return False
            job.add_progress()
        return True

    def __ProcessNormalList(self, name_list, copy=False, job=nulljob):
        name_list = [paths for paths in name_list if (paths[0] != paths[1]) and io.exists(paths[0])]
        conflicts = []
        tmpdir = None
        job.start_job(len(name_list))
        for source, dest in name_list:
            try:
                if io.exists(dest):
                    if not tmpdir:
                        tmpdir = Path(tempfile.mkdtemp())
                    newdest = tmpdir + dest[self.destination:]
                    conflicts.append((newdest, dest, source))
                    dest = newdest
                if not io.exists(dest[:-1]):
                    io.makedirs(dest[:-1])
                if copy:
                    io.copy(source, dest)
                else:
                    io.move(source, dest)
            except (OSError, IOError) as e:
                print("Warning: Error %r occured while processing %r to %r."\
                    % (e, str(source), str(dest)))
            job.add_progress()
        for source, dest, old_source in conflicts:
            if not io.exists(dest):
                io.rename(source, dest)
            elif not io.exists(old_source):
                io.rename(source, old_source)

    #---Public
    def copy(self, job=nulljob):
        return self.__Perform(True, job)

    def rename(self, job=nulljob):
        return self.__Perform(False, job)

    #---Events
    def OnNeedCD(self, location):
        #The result of OnNeedCD can be a string or a Path or None.
        pass

    #---Properties
    name_list = []

class BufferError(Exception): pass
class AlreadyInBuffer(BufferError): pass
class FileIsPurged(BufferError): pass
class NotEnoughSpaceInBuffer(BufferError): pass

class Buffer(object):
    """Object to manage the transfer of files from removables medias to other removable medias

    When initializing Buffer, you give it a max buffer size, and then add all
    virtual files, along with their source, and their destination.

    Here is a sample hypothetical use of Buffer:

    b = Buffer(2)
    b.AddFiles(
        (f1,'source1','dest1',1),
        (f2,'source2','dest1',1),
        (f3,'source2','dest2',1),
    )
    for dest in ('dest1','dest2'):
        for t in b.DoBufferingFor(dest):
            file,source = t
            CopyFromSourceToTmpDir(file,source) #it copies file in /tmp/<source>
        BurnAllFilesIn('/tmp/%s' % source)
        DeleteAllFilesIn('/tmp/%s' % source)
        b.PurgeBufferOf(dest)

    """
    #---Override
    def __init__(self, size):
        self.size = size
        self.__sources = {}
        self.__destinations = {}
        self.__content = {}
        self.__purged = {}
        self.__space_taken = 0

    #---Private
    def __BufferFile(self, file):
        if (file[3] > self.space_left):
            raise NotEnoughSpaceInBuffer
        if (file[0] in self.__content):
            raise AlreadyInBuffer
        if (file[0] in self.__purged):
            raise FileIsPurged
        self.__content[file[0]] = file
        self.__space_taken += file[3]
        return file

    def __GetContent(self):
        return list(self.__content.values())

    def __PurgeFile(self, file):
        try:
            del self.__content[file[0]]
            self.__purged[file[0]] = file
            self.__space_taken -= file[3]
            return file
        except KeyError:
            pass

    #---Public
    def AddFiles(self, files):
        """Add 'files' to self

        Where 'files' is a list of tuples with the format (id,source,dest,size)

        id: id can be anything, as long as it uniquely identify the file. What is
        convenient to use is, for example, a fs.File instance.
        source: A string defining a source.
        dest: A string defining a destination.
        size: (int) The size of the file in bytes.
        """
        for file in files:
            id, source, dest, size = file
            if source not in self.__sources:
                self.__sources[source] = []
            self.__sources[source].append(file)
            if dest not in self.__destinations:
                self.__destinations[dest] = []
            self.__destinations[dest].append(file)

    def DoBufferingFor(self, destination):
        try:
            files = [f for f in self.__destinations[destination] if f[0] not in self.__content]
            for file in files:
                self.__BufferFile(file)
            sources = self.GetSources(files)
            for source in sources:
                source_files = self.__sources[source]
                for file in source_files:
                    try:
                        files.append(self.__BufferFile(file))
                    except BufferError:
                        pass
            return files
        except KeyError:
            return []

    def GetDestinations(files):
        result = []
        for file in files:
            if file[2] not in result:
                result.append(file[2])
        return result
    GetDestinations = staticmethod(GetDestinations)

    def GetMaximumBytesRequired(self):
        dest_sizes = []
        for files in list(self.__destinations.values()):
            size_sum = sum(f[3] for f in files)
            dest_sizes.append(size_sum)
        return sum(dest_sizes)

    def GetMinimumBytesRequired(self):
        dest_sizes = []
        for files in list(self.__destinations.values()):
            size_sum = sum(f[3] for f in files)
            dest_sizes.append(size_sum)
        return max(dest_sizes)

    def GetSources(files):
        result = []
        for file in files:
            if file[1] not in result:
                result.append(file[1])
        return result
    GetSources = staticmethod(GetSources)

    def PurgeBufferOf(self,destination):
        try:
            result = [self.__PurgeFile(file) for file in self.__destinations[destination]]
            return result
        except KeyError:
            return []

    #---Properties
    content     = property(__GetContent)
    size        = 0
    space_left  = property(lambda x: x.size - x.__space_taken)
    space_taken = property(lambda x: x.__space_taken)
