#import <Cocoa/Cocoa.h>
#import "Wizard.h"

@interface PathChoicePage : WizPage
{
    IBOutlet NSTextField *pathText;
}
- (IBAction)choosePath:(id)sender;
@end
