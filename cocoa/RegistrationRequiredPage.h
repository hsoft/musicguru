#import <Cocoa/Cocoa.h>
#import "Wizard.h"
#import "PyMusicGuru.h"

@interface RegistrationRequiredPage : WizPage
{
    PyMusicGuru *py;
}
- (IBAction)buyNow:(id)sender;
- (IBAction)enterCode:(id)sender;
@end
