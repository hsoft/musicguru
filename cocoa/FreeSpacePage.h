#import <Cocoa/Cocoa.h>
#import "Wizard.h"
#import "PyMusicGuru.h"

@interface FreeSpacePage : WizPage
{
    IBOutlet NSButton *freeSpaceImage;
    IBOutlet NSTextField *freeSpaceLabel;
    IBOutlet NSTextField *messageLabel;
    IBOutlet NSTextField *minimumLabel;
    IBOutlet NSTextField *recommendedLabel;
    
    PyMusicGuru *py;
}
- (IBAction)evaluateFreeSpace:(id)sender;

- (BOOL)evaluateFreeSpace;
@end
