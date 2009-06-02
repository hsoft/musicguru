/* DesignWindow */

#import <Cocoa/Cocoa.h>
#import <cocoalib/Outline.h>
#import <cocoalib/Table.h>
#import "DetailsPanel.h"
#import "PyMusicGuru.h"
#import "MaterializeWizard.h"

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
    MaterializeWizard *_wiz;
}
- (id)initWithParentApp:(id)aApp;

- (IBAction)massRename:(id)sender;
- (IBAction)materialize:(id)sender;
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

- (void)materializeWizardCallback:(MaterializeWizard *)aWizard;
- (void)refresh;
- (void)refreshStats;
- (void)setDetailsPanel:(DetailsPanel *)aDetailsPanel;
- (BOOL)validateAction:(SEL)aAction fromToolbar:(BOOL)aFromToolbar;
@end
