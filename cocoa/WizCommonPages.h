/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "MessagePage.h"
#import "ProgressPage.h"

@interface WizCommonPages : NSObject
{
    IBOutlet MessagePage *messagePage;
    IBOutlet ProgressPage *progressPage;
}
- (MessagePage *)messagePage;
- (ProgressPage *)progressPage;
@end
