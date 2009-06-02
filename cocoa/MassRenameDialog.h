/* RenamingModelDialog */

#import <Cocoa/Cocoa.h>
#import "PyMusicGuru.h"

@interface MassRenameDialog : NSWindowController
{
    IBOutlet NSTextField *customModelText;
    IBOutlet NSMatrix *modelSelector;
    IBOutlet NSTextField *nameAfterLabel;
    IBOutlet NSTextField *nameBeforeLabel;
    IBOutlet NSMatrix *whitespaceSelector;
    
    PyMassRenamePanel *py;
}
- (id)initWithPyMassRenamePanel:(PyMassRenamePanel *)aPy;
- (void)dealloc;

- (IBAction)cancel:(id)sender;
- (IBAction)changeExampleSong:(id)sender;
- (IBAction)displayExampleSong:(id)sender;
- (IBAction)ok:(id)sender;

- (BOOL)run;
@end
