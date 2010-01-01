/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "../cocoalib/PyApp.h"

@interface PyMassRenamePanel : NSObject
- (void)changeExampleSong;
- (NSString *)getExampleDisplayAfter;
- (NSString *)getExampleDisplayBefore;
- (NSString *)getModel;
- (NSNumber *)getWhitespace;
- (void)setCustomModel:(NSString *)aModel;
- (void)setModelSelectedRow:(NSNumber *)aRow;
- (void)setWhitespaceSelectedRow:(NSNumber *)aRow;
@end
            
@interface PySplitPanel : NSObject
- (NSString *)getGroupingExample;
- (NSNumber *)getCapacity;
- (NSNumber *)getGroupingLevel;
- (NSString *)getModel;
- (void)setCapacitySelectedRow:(NSNumber *)aRow;
- (void)setCustomCapacity:(NSNumber *)aCapacity;
- (void)setCustomModel:(NSString *)aModel;
- (void)setGroupingLevel:(NSNumber *)aGroupingLevel;
- (void)setModelSelectedRow:(NSNumber *)aRow;
@end

@interface PyMusicGuru : PyApp
//Locations
- (NSNumber *)addLocationWithPath:(NSString *)aPath name:(NSString *)aName removeable:(NSNumber *)aRemoveable;
- (NSString *)canAddLocationWithPath:(NSString *)aPath name:(NSString *)aName;
- (NSArray *)locationNamesInBoard:(NSNumber *)aInBoard writable:(NSNumber *)aWritableOnly;
- (void)removeLocationNamed:(NSString *)aName;
- (void)setPath:(NSString *)path ofLocationNamed:(NSString *)name;
- (void)toggleLocation:(NSNumber *)index;
- (void)updateCollection;
- (void)updateLocationNamed:(NSString *)name;
//Board
- (NSNumber *)conflictCount;
- (void)emptyBoard;
- (NSString *)getBoardStats;
- (PyMassRenamePanel *)getMassRenamePanel;
- (PySplitPanel *)getSplitPanel;
- (NSNumber *)isBoardSplitted;
- (NSNumber *)isNodeConflicted:(NSArray *)aNodePath;
- (void)massRenameWithModel:(NSString *)aModel whitespaceType:(NSNumber *)aWhitespace;
- (NSNumber *)moveConflicts;
- (NSNumber *)moveConflictsAndOriginals;
- (void)moveToIgnoreBox:(NSArray *)aNodePaths;
- (NSString *)newFolderIn:(NSArray *)aNodePath;
- (NSNumber *)performDragFrom:(NSNumber *)aSourceTag withNodes:(NSArray *)aSourceNodePaths to:(NSNumber *)aDestTag withNode:(NSArray *)aDestNodePath;
- (void)removeEmptyFolders;
- (NSString *)renameNode:(NSArray *)aNodePath to:(NSString *)aNewName;
- (void)selectBoardSongs:(NSArray *)selected;
- (void)splitWithModel:(NSString *)aModel capacity:(NSNumber *)aCapacity groupingLevel:(NSNumber *)aGroupingLevel;
- (void)switchConflictAndOriginal:(NSArray *)aNodePath;
- (void)unsplit;
//Materialize
- (NSNumber *)addCurrentDiskToMPLOverwrite:(NSNumber *)aOverwrite; //Returns True if the location has been added.
- (void)burnCurrentDiskWithWindow:(NSWindow *)aWindow;
- (void)cleanBuffer;
- (void)copyOrMove:(NSNumber *)aCopy toPath:(NSString *)aPath onNeedCDPanel:(id)aPanel;
- (NSNumber *)ejectCDIfNotBlank; //Returns True if a blank CD is in the drive, False if not (and if it returns false, it means that the current CD has been ejected.)
- (void)fetchSourceSongsWithNeedCDPanel:(id)aPanel;
- (NSArray *)getBurnBufferSizes; // 0: Free Bytes on disk, 1: Minimum, 2: Recommended. 3,4,5: formatted sizes
- (NSString *)getDestinationDiskName;
- (NSNumber *)isFinishedBurning;
- (NSNumber *)prepareBurning; //True: Uses buffering (show free disk space page) False: doesn't.
- (void)prepareNextCDToBurn;
- (void)renameInRespectiveLocations;
//Misc
- (NSNumber *)isNodeContainer:(NSArray *)aNodePath;

- (void)setProgressController:(id)progress;
@end