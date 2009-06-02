/* ProgressPage */

#import <Cocoa/Cocoa.h>
#import "Wizard.h"

@interface ProgressPage : WizPage
{
    IBOutlet NSTextField *messageLabel;
    IBOutlet NSProgressIndicator *progress;
}
- (void)setJobDesc:(NSString *)desc;
- (BOOL)update:(int)newProgress;
- (NSNumber *)pyUpdate:(NSNumber *)newProgress;
- (void)processAppEvents;
@end
