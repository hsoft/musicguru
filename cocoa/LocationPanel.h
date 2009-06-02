#import <Cocoa/Cocoa.h>
#import <cocoalib/Table.h>
#import "AddLocationWindow.h"
#import "PyMusicGuru.h"

@interface LocationPanel : NSWindowController
{
    IBOutlet NSButton *changeLocationPathButton;
    IBOutlet TableView *locationsTable;
    IBOutlet NSTextField *pathLabel;
    IBOutlet NSTextField *typeLabel;
    
    AddLocationWindow *_addLocation;
    PyMusicGuru *py;
}
- (id)initWithPy:(PyApp *)aPy;
- (BOOL)canMaterialize;
- (void)updateLocationDetails;

- (IBAction)addLocation:(id)sender;
- (IBAction)changeLocationPath:(id)sender;
- (IBAction)markLocation:(id)sender;
- (IBAction)removeLocation:(id)sender;
- (IBAction)updateCollection:(id)sender;

/* Notifications */
- (void)locationTableSelectionChanged:(NSNotification *)aNotification;
- (void)MPLChanged:(NSNotification *)aNotification;
@end
