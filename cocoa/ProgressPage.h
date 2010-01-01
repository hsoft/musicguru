/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

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
