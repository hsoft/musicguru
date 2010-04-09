/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "Outline.h"
#import "Table.h"
#import "DetailsPanel.h"
#import "PyMusicGuru.h"

@interface DesignOutlineView : DraggableOutlineView
{
    BOOL _alternateDragging;
}
- (BOOL)alternateDragging;
@end

@interface DesignWindow : NSWindowController
{
    IBOutlet NSMenu *actionMenu;
    IBOutlet NSView *actionMenuView;
    IBOutlet DesignOutlineView *browserOutline;
    IBOutlet DesignOutlineView *ignoreBoxOutline;
    IBOutlet NSPanel *ignoreBoxPanel;
    IBOutlet NSTextField *statsLabel;
    
    id _app;
    DetailsPanel *_detailsPanel;
    OVNode *_editedNode;
    NSTextField *_editor;
    long long _mediaCapacity;
    PyMusicGuru *py;
}
- (id)initWithParentApp:(id)aApp;

- (IBAction)massRename:(id)sender;
- (IBAction)materializeInPlace:(id)sender;
- (IBAction)copyToLocation:(id)sender;
- (IBAction)moveToLocation:(id)sender;
- (IBAction)moveConflicts:(id)sender;
- (IBAction)moveConflictsAndOriginals:(id)sender;
- (IBAction)moveToIgnoreBox:(id)sender;
- (IBAction)newFolder:(id)sender;
- (IBAction)removeEmptyFolders:(id)sender;
- (IBAction)renameClicked:(id)sender;
- (IBAction)renameSelected:(id)sender;
- (IBAction)selectSong:(id)sender;
- (IBAction)showIgnoreBox:(id)sender;
- (IBAction)split:(id)sender;
- (IBAction)switchConflictAndOriginal:(id)sender;
- (IBAction)unsplit:(id)sender;

- (void)refresh;
- (void)refreshStats;
- (void)setDetailsPanel:(DetailsPanel *)aDetailsPanel;
- (BOOL)validateAction:(SEL)aAction fromToolbar:(BOOL)aFromToolbar;
@end
