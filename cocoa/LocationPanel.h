/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "Table.h"
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
- (id)initWithPy:(PyMusicGuru *)aPy;
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
