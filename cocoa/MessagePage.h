/* MessagePage */

#import <Cocoa/Cocoa.h>
#import "Wizard.h"

@interface MessagePage : WizPage
{
    IBOutlet NSTextField *messageLabel;
}
- (void)setMessage:(NSString *)aMessage;
@end
